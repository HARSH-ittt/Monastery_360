#!/usr/bin/env python3
"""
Test script to verify Mistral integration with Ollama
Run this script to test if Mistral is properly configured and responding
"""

import requests
import json
import time

def test_mistral_connection():
    """Test if Mistral model is available and responding"""
    print("🔍 Testing Mistral integration with Ollama...")
    
    # Test 1: Check if Ollama is running
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            mistral_models = [m for m in models if 'mistral' in m.get('name', '').lower()]
            if mistral_models:
                print(f"✅ Ollama is running and Mistral models found: {[m['name'] for m in mistral_models]}")
            else:
                print("❌ Ollama is running but no Mistral models found")
                print("Available models:", [m['name'] for m in models])
                return False
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False
    
    # Test 2: Test Mistral generation
    print("\n🤖 Testing Mistral generation...")
    try:
        payload = {
            'model': 'mistral',
            'prompt': 'Hello! Can you tell me about Sikkim monasteries in one sentence?',
            'stream': False,
            'options': {
                'temperature': 0.7,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'num_ctx': 4096,
                'num_predict': 100
            }
        }
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Mistral response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"❌ Mistral generation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Mistral generation: {e}")
        return False

def test_streaming():
    """Test streaming functionality"""
    print("\n🌊 Testing streaming functionality...")
    try:
        payload = {
            'model': 'mistral',
            'prompt': 'Tell me about Rumtek Monastery in Sikkim.',
            'stream': True,
            'options': {
                'temperature': 0.7,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'num_ctx': 4096,
                'num_predict': 200
            }
        }
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Streaming response:")
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        if 'response' in json_data:
                            chunk = json_data['response']
                            print(chunk, end='', flush=True)
                            full_response += chunk
                        if json_data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            print(f"\n\n✅ Streaming completed. Full response length: {len(full_response)} characters")
            return True
        else:
            print(f"❌ Streaming failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing streaming: {e}")
        return False

def test_backend_server():
    """Test if the backend server can be started"""
    print("\n🚀 Testing backend server configuration...")
    
    # Check if required files exist
    import os
    files_to_check = [
        'backend/api/server.py',
        'backend/api/server.js',
        'backend/requirements.txt',
        'backend/package.json'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ All required backend files present")
    return True

if __name__ == "__main__":
    print("🧪 Mistral Integration Test Suite")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Backend Files", test_backend_server),
        ("Mistral Connection", test_mistral_connection),
        ("Streaming", test_streaming)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Mistral integration is ready to use.")
        print("\n📝 Next steps:")
        print("1. Start Ollama: ollama serve")
        print("2. Start Python server: python backend/api/server.py")
        print("3. Or start Node.js server: node backend/api/server.js")
        print("4. Open frontend/index.html in your browser")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
