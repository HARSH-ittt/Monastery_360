#!/usr/bin/env python3
"""
Test script for the chatbot functionality
This script tests the complete chatbot system
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def test_ollama():
    """Test if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            mistral_models = [m for m in models if 'mistral' in m.get('name', '').lower()]
            if mistral_models:
                print(f"✅ Ollama is running with Mistral: {[m['name'] for m in mistral_models]}")
                return True
            else:
                print("❌ Ollama is running but no Mistral models found")
                return False
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_server():
    """Test if the Python server is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ Python server is running")
            return True
        else:
            print(f"❌ Python server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Python server: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    try:
        payload = {
            'message': 'Hello, tell me about Sikkim monasteries',
            'lang': 'en'
        }
        
        response = requests.post(
            'http://localhost:3000/chat',
            json=payload,
            timeout=30,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Chat endpoint is working")
            
            # Test streaming response
            print("📝 Testing streaming response:")
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data = line_str[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                print("\n✅ Streaming completed successfully")
                                break
                            else:
                                print(data, end='', flush=True)
                    except Exception as e:
                        print(f"\n⚠️  Error parsing line: {e}")
                        continue
            
            return True
        else:
            print(f"❌ Chat endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
        return False

def start_server():
    """Start the Python server"""
    print("🚀 Starting Python server...")
    try:
        # Start server in background
        process = subprocess.Popen(
            [sys.executable, 'backend/api/server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(10):
            time.sleep(1)
            if test_server():
                print("✅ Server started successfully")
                return process
            print(f"   Waiting... ({i+1}/10)")
        
        print("❌ Server failed to start within 10 seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def main():
    print("🤖 Chatbot System Test")
    print("=" * 40)
    
    # Test Ollama
    print("\n1. Testing Ollama...")
    if not test_ollama():
        print("\n❌ Ollama is not running. Please start it first:")
        print("   ollama serve")
        return False
    
    # Test server
    print("\n2. Testing Python server...")
    server_process = None
    if not test_server():
        print("   Server not running, starting it...")
        server_process = start_server()
        if not server_process:
            return False
    
    # Test chat endpoint
    print("\n3. Testing chat endpoint...")
    if not test_chat_endpoint():
        print("\n❌ Chat endpoint test failed")
        if server_process:
            server_process.terminate()
        return False
    
    print("\n🎉 All tests passed! Chatbot is working correctly.")
    print("\n📝 Next steps:")
    print("1. Open frontend/index.html in your browser")
    print("2. Click the AI Assistant button")
    print("3. Try asking: 'Tell me about Rumtek Monastery'")
    
    if server_process:
        print("\n⚠️  Server is running in background. Press Ctrl+C to stop.")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
    
    return True

if __name__ == "__main__":
    main()

