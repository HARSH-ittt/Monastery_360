from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import json
import os
import uuid
import time
from werkzeug.utils import secure_filename
from datetime import datetime
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# Removed MySQL dependency
# Import Sikkim context for enhanced responses
from api.sikkim_context import get_sikkim_facts

app = Flask(__name__, static_folder='../../frontend', static_url_path='')
CORS(app)

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads', 'research')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'tiff', 'bmp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    """Simple chat endpoint that returns a static response for testing"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # For debugging
        print(f"Received message: {message}")
        print(f"Request data: {data}")
        
        # Check if this is a test request from start_chatbot.py
        if request.headers.get('User-Agent') and 'python-requests' in request.headers.get('User-Agent'):
            # For test requests, return a simple JSON response
            return jsonify({
                'response': "Hello! I'm the Sikkim Tourism Assistant. This is a test response.",
                'status': 'success'
            })
        
        # For normal requests, return streaming response
        def generate():
            # Send a welcome message
            yield "data: Hello! I'm the Sikkim Tourism Assistant.\n\n"
            time.sleep(0.2)
            yield "data: I can help you with information about Sikkim's tourist destinations, culture, and more.\n\n"
            time.sleep(0.2)
            yield "data: This is a test response to verify the chat functionality is working.\n\n"
            time.sleep(0.2)
            yield f"data: Your message was: '{message}'\n\n"
            time.sleep(0.2)
            yield "data: [DONE]\n\n"

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to process chat request: {str(e)}'}), 500


@app.route('/chat-stream')
def chat_stream():
    try:
        message = request.args.get("message", "")

        payload = {
            'model': 'mistral',
            'prompt': message,
            'stream': True,
            'options': {
                'temperature': 0.7,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'num_ctx': 2048,
                'num_predict': 150
            }
        }

        ollama_response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            stream=True,
            timeout=30
        )

        def generate():
            for line in ollama_response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        if 'response' in json_data:
                            yield f"data: {json_data['response']}\n\n"
                        if json_data.get('done', False):
                            yield "data: [DONE]\n\n"
                            break
                    except json.JSONDecodeError:
                        continue

        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to connect to Ollama'}), 500

# Research Submission Endpoints
@app.route('/api/research/submit', methods=['POST'])
def submit_research():
    """Submit research data"""
    try:
        # MySQL dependency removed
        return jsonify({'success': True, 'message': 'Research submission feature disabled (MySQL dependency removed)'}), 200
    except Exception as e:
        print(f"Error submitting research: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/research/submissions', methods=['GET'])
def get_research_submissions():
    """Get research submissions"""
    try:
        # MySQL dependency removed
        return jsonify({'submissions': [], 'message': 'Research submissions feature disabled (MySQL dependency removed)'}), 200
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/research/categories', methods=['GET'])
def get_categories():
    """Get research categories"""
    try:
        # MySQL dependency removed
        return jsonify({'categories': [], 'message': 'Research categories feature disabled (MySQL dependency removed)'}), 200
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/research/file/<int:submission_id>', methods=['GET'])
def get_research_file(submission_id):
    """Serve research file for download"""
    try:
        # MySQL dependency removed
        return jsonify({'error': 'Research file feature disabled (MySQL dependency removed)'}), 404
    except Exception as e:
        print(f"Error serving file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Database initialization removed to eliminate MySQL dependency

if __name__ == '__main__':
    # Skip database initialization
    print("✅ Streaming server running at http://localhost:3000")
    # Use 0.0.0.0 to allow external connections
    app.run(host='0.0.0.0', port=3000, debug=False)
