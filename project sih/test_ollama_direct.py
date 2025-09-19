#!/usr/bin/env python3
"""
Test Ollama connection directly
"""

import requests
import json

def test_ollama_direct():
    """Test Ollama connection directly"""
    print("🔍 Testing Ollama connection directly...")
    
    try:
        payload = {
            'model': 'mistral',
            'prompt': 'Hello, tell me about Sikkim in one sentence.',
            'stream': False,
            'options': {
                'temperature': 0.7,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'num_ctx': 2048,
                'num_predict': 50
            }
        }
        
        print("📤 Sending request to Ollama...")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"❌ Ollama error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_ollama_streaming():
    """Test Ollama streaming"""
    print("\n🔍 Testing Ollama streaming...")
    
    try:
        payload = {
            'model': 'mistral',
            'prompt': 'Tell me about Rumtek Monastery.',
            'stream': True,
            'options': {
                'temperature': 0.7,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'num_ctx': 2048,
                'num_predict': 100
            }
        }
        
        print("📤 Sending streaming request to Ollama...")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            stream=True,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("📝 Streaming response:")
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        if 'response' in json_data:
                            print(json_data['response'], end='', flush=True)
                        if json_data.get('done', False):
                            print("\n✅ Streaming completed")
                            break
                    except json.JSONDecodeError:
                        continue
            return True
        else:
            print(f"❌ Ollama streaming error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama streaming failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Ollama Direct Test")
    print("=" * 30)
    
    # Test 1: Direct Ollama connection
    ollama_ok = test_ollama_direct()
    
    # Test 2: Ollama streaming
    streaming_ok = test_ollama_streaming()
    
    if ollama_ok and streaming_ok:
        print("\n🎉 Ollama is working correctly!")
    else:
        print("\n❌ Ollama has issues. Check the errors above.")

