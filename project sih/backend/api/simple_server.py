from flask import Flask, request, Response, jsonify, stream_with_context
from flask_cors import CORS
import time
import os
import random
import requests
import json
import difflib

app = Flask(__name__, static_folder='../../frontend', static_url_path='')
CORS(app)

# Ollama API configuration
OLLAMA_API_BASE = "http://localhost:11434/api"
MISTRAL_MODEL = "mistral"

# Load fixed Q&A from JSON file
def load_fixed_qa():
    """Load fixed questions and answers from JSON file"""
    try:
        qa_file_path = os.path.join(os.path.dirname(__file__), 'fixed_qa.json')
        with open(qa_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fixed Q&A: {e}")
        return []

# Load fixed Q&A at startup
FIXED_QA = load_fixed_qa()
print(f"Loaded {len(FIXED_QA)} fixed Q&A pairs")

def find_best_match(user_message, threshold=0.6):
    """Find the best matching question from fixed Q&A"""
    user_message_lower = user_message.lower().strip()
    
    best_match = None
    best_ratio = 0
    
    for qa in FIXED_QA:
        question_lower = qa['question'].lower().strip()
        
        # Calculate similarity ratio
        ratio = difflib.SequenceMatcher(None, user_message_lower, question_lower).ratio()
        
        # Also check if user message contains key words from the question
        question_words = set(question_lower.split())
        user_words = set(user_message_lower.split())
        
        # If there's significant word overlap, boost the ratio
        word_overlap = len(question_words.intersection(user_words)) / len(question_words)
        if word_overlap > 0.5:  # More than 50% word overlap
            ratio = max(ratio, word_overlap)
        
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = qa
    
    return best_match, best_ratio

# Dictionary of predefined responses based on keywords (fallback if Mistral is unavailable)
RESPONSES = {
    "hello": [
        "Hello! Welcome to the Sikkim Tourism Assistant. How can I help you today?",
        "Hi there! I'm here to help with your questions about Sikkim. What would you like to know?",
        "Greetings! I'm your Sikkim guide. What are you interested in learning about?"
    ],
    "monastery": [
        "Sikkim is home to many beautiful monasteries. Some famous ones include Rumtek, Pemayangtse, and Tashiding monasteries.",
        "The monasteries in Sikkim are centers of Buddhist learning and culture. They feature colorful murals, ancient artifacts, and peaceful surroundings.",
        "Sikkim's monasteries are perched on hilltops offering spectacular views. Many of them date back several centuries and showcase unique Tibetan architecture."
    ],
    "food": [
        "Sikkim's cuisine is influenced by Tibetan, Nepali, and indigenous traditions. Momos, thukpa, and gundruk are popular dishes.",
        "You must try Sikkim's traditional foods like sel roti (rice bread), phagshapa (pork with radish), and chhurpi (yak cheese).",
        "Sikkim is known for its organic produce. The local dishes often feature fresh ingredients like cardamom, ginger, and various mountain herbs."
    ],
    "weather": [
        "Sikkim has diverse climate zones. The best time to visit is from March to May or October to December when the weather is pleasant.",
        "Summers (April-June) are mild in Sikkim, while winters (December-February) can be quite cold, especially in higher elevations.",
        "Monsoon season (June-September) brings heavy rainfall to Sikkim, making some areas difficult to access due to landslides."
    ],
    "trekking": [
        "Sikkim offers amazing trekking routes like the Goecha La trek, Green Lake trek, and Dzongri trek with views of Kanchenjunga.",
        "Trekking in Sikkim takes you through rhododendron forests, alpine meadows, and offers glimpses of rare wildlife.",
        "The best seasons for trekking in Sikkim are spring (March-May) and autumn (October-November) when visibility is good and weather is stable."
    ],
    "festival": [
        "Losar (Tibetan New Year), Saga Dawa, and Pang Lhabsol are some of the major festivals celebrated in Sikkim.",
        "Sikkim's festivals feature colorful mask dances, traditional music, and elaborate religious ceremonies.",
        "During festivals in Sikkim, you can witness unique cultural performances and taste special festive foods."
    ]
}

# Default responses when no keywords match or Mistral is unavailable
DEFAULT_RESPONSES = [
    "Sikkim is a beautiful state in northeastern India known for its stunning landscapes and rich culture.",
    "As your Sikkim Tourism Assistant, I can help with information about places to visit, local customs, and travel tips.",
    "Sikkim offers diverse experiences from mountain views to cultural immersion. What specific aspect interests you?",
    "I'd be happy to tell you more about Sikkim's attractions, cuisine, or festivals. Please ask something specific."
]

# Check if Ollama is available and Mistral model is loaded
def is_mistral_available():
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return any('mistral' in model.get('name', '').lower() for model in models)
        return False
    except:
        print("⚠️ Cannot connect to Ollama service")
        return False

@app.route('/')
def serve_index():
    try:
        return app.send_static_file('index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        # Fallback: serve from absolute path
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'index.html')
        if os.path.exists(frontend_path):
            with open(frontend_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Error: Could not find index.html. Looking for: {frontend_path}", 404

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to check if server is working"""
    return jsonify({'status': 'ok', 'message': 'Server is working'})

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint that returns responses using fixed Q&A, Mistral model, or fallback to predefined responses"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        original_message = message
        message_lower = message.lower()
        
        print(f"Received message: {message}")
        
        # First, check for fixed Q&A matches
        fixed_match, match_ratio = find_best_match(message)
        if fixed_match:
            print(f"🎯 Found fixed Q&A match (ratio: {match_ratio:.2f}): {fixed_match['question']}")
            response = fixed_match['answer']
            print(f"Sending fixed response: {response[:50]}...")
            return jsonify({
                'response': response,
                'status': 'success',
                'source': 'fixed_qa'
            })
        
        # Check if Mistral is available
        use_mistral = is_mistral_available()
        
        if use_mistral:
            print("🤖 Using Mistral model for response")
            try:
                # Prepare context for Sikkim tourism assistant
                prompt = f"""You are a helpful Sikkim Tourism Assistant that specializes in providing information about Sikkim's monasteries, culture, food, weather, trekking, and festivals.
                
                User message: {message}
                
                Provide a helpful, informative response about Sikkim based on the user's query. Keep your response concise and focused on Sikkim tourism."""
                
                # Call Mistral model via Ollama API
                response_data = requests.post(
                    f"{OLLAMA_API_BASE}/generate",
                    json={
                        "model": MISTRAL_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "repeat_penalty": 1.1,
                            "num_ctx": 4096,
                            "num_predict": 512
                        }
                    },
                    timeout=10
                )
                
                if response_data.status_code == 200:
                    response = response_data.json().get('response', '')
                    # Clean up any potential formatting issues
                    response = response.strip()
                    print(f"Sending Mistral response: {response[:50]}...")
                    return jsonify({
                        'response': response,
                        'status': 'success',
                        'source': 'mistral'
                    })
                else:
                    print(f"⚠️ Mistral API returned status {response_data.status_code}")
                    raise Exception("Failed to get response from Mistral")
                    
            except Exception as e:
                print(f"⚠️ Error using Mistral: {e}")
                # Fall back to predefined responses
                use_mistral = False
        
        # Fallback to predefined responses if Mistral is unavailable or failed
        if not use_mistral:
            print("📝 Using predefined responses")
            # Debug print to see what's happening
            print(f"Looking for keywords in: {message_lower}")
            
            # Check for specific keywords with more flexible matching
            if "monastery" in message_lower or "monasteries" in message_lower:
                response = random.choice(RESPONSES["monastery"])
            elif "food" in message_lower or "cuisine" in message_lower or "eat" in message_lower:
                response = random.choice(RESPONSES["food"])
            elif "weather" in message_lower or "climate" in message_lower or "season" in message_lower:
                response = random.choice(RESPONSES["weather"])
            elif "trek" in message_lower or "trekking" in message_lower or "hike" in message_lower:
                response = random.choice(RESPONSES["trekking"])
            elif "festival" in message_lower or "celebration" in message_lower or "event" in message_lower:
                response = random.choice(RESPONSES["festival"])
            elif "hello" in message_lower or "hi" in message_lower or "greet" in message_lower:
                response = random.choice(RESPONSES["hello"])
            else:
                # Use default response if no keywords match
                response = random.choice(DEFAULT_RESPONSES)
            
            response += f"\n\nYou asked about: '{original_message}'"
            
            # Debug print the response
            print(f"Sending predefined response: {response[:50]}...")
            
            # Return a simple JSON response
            return jsonify({
                'response': response,
                'status': 'success',
                'source': 'predefined'
            })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'response': "I'm sorry, I encountered an error processing your request.",
            'status': 'error',
            'error': str(e)
        }), 500

# Add streaming endpoint for advanced UI features
@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint that returns responses using fixed Q&A or Mistral model"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        print(f"Received streaming request: {message}")
        
        # First, check for fixed Q&A matches
        fixed_match, match_ratio = find_best_match(message)
        if fixed_match:
            print(f"🎯 Found fixed Q&A match (ratio: {match_ratio:.2f}): {fixed_match['question']}")
            
            def generate_fixed_response():
                response_text = fixed_match['answer']
                # Simulate streaming by sending the response in chunks
                words = response_text.split()
                for i, word in enumerate(words):
                    yield f"data: {json.dumps({'text': word + ' '})}\n\n"
                    time.sleep(0.05)  # Small delay to simulate streaming
                yield f"data: {json.dumps({'text': '', 'done': True})}\n\n"
            
            return Response(stream_with_context(generate_fixed_response()), mimetype='text/event-stream')
        
        # Check if Mistral is available
        if not is_mistral_available():
            return jsonify({
                'response': "Streaming is only available with Mistral model. The model is currently unavailable.",
                'status': 'error'
            }), 503
        
        def generate():
            try:
                # Prepare context for Sikkim tourism assistant
                prompt = f"""You are a helpful Sikkim Tourism Assistant that specializes in providing information about Sikkim's monasteries, culture, food, weather, trekking, and festivals.
                
                User message: {message}
                
                Provide a helpful, informative response about Sikkim based on the user's query. Keep your response concise and focused on Sikkim tourism."""
                
                # Call Mistral model via Ollama API with streaming
                response = requests.post(
                    f"{OLLAMA_API_BASE}/generate",
                    json={
                        "model": MISTRAL_MODEL,
                        "prompt": prompt,
                        "stream": True,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "repeat_penalty": 1.1,
                            "num_ctx": 4096,
                            "num_predict": 512
                        }
                    },
                    stream=True,
                    timeout=30
                )
                
                # Stream the response
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            yield f"data: {json.dumps({'text': chunk['response']})}\n\n"
                
                # End of stream
                yield f"data: {json.dumps({'text': '', 'done': True})}\n\n"
                
            except Exception as e:
                print(f"Error in streaming: {e}")
                yield f"data: {json.dumps({'text': '', 'error': str(e), 'done': True})}\n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    
    except Exception as e:
        print(f"Error setting up streaming: {e}")
        return jsonify({
            'response': "Error setting up streaming response",
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print(f"🚀 Starting server at http://localhost:3000")
    print(f"🤖 Mistral model {'available' if is_mistral_available() else 'not available'}")
    app.run(host='0.0.0.0', port=3000, debug=False)