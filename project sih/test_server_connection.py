#!/usr/bin/env python3
"""
Test server connection and diagnose issues
"""

import requests
import json
import time

def test_server():
    """Test the server endpoints"""
    base_url = "http://localhost:3000"
    
    print("🔍 Testing server connection...")
    
    # Test 1: Basic connection
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Content type: {response.headers.get('content-type', 'unknown')}")
            print(f"   Content length: {len(response.text)}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test 2: Chat endpoint
    try:
        payload = {"message": "Hello", "lang": "en"}
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            timeout=10,
            stream=True
        )
        print(f"✅ Chat endpoint: {response.status_code}")
        
        if response.status_code == 200:
            print("   Testing streaming response...")
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = line_str[6:]
                        if data == '[DONE]':
                            print("   ✅ Streaming completed")
                            break
                        else:
                            print(f"   📝 Response chunk: {data[:50]}...")
        else:
            print(f"   ❌ Chat endpoint error: {response.text}")
            
    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
        return False
    
    return True

def test_ollama():
    """Test Ollama connection"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            mistral_models = [m for m in models if 'mistral' in m.get('name', '').lower()]
            if mistral_models:
                print(f"✅ Ollama running with Mistral: {[m['name'] for m in mistral_models]}")
                return True
            else:
                print("❌ Ollama running but no Mistral models found")
                return False
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Server Connection Test")
    print("=" * 40)
    
    print("\n1. Testing Ollama...")
    ollama_ok = test_ollama()
    
    print("\n2. Testing Python server...")
    server_ok = test_server()
    
    if ollama_ok and server_ok:
        print("\n🎉 All tests passed! Server is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")

