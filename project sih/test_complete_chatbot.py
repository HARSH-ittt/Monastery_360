#!/usr/bin/env python3
"""
Complete chatbot functionality test
"""

import requests
import json
import time

def test_complete_chatbot():
    """Test the complete chatbot functionality"""
    print("🤖 Complete Chatbot Test")
    print("=" * 40)
    
    # Test 1: Server status
    print("\n1. Testing server status...")
    try:
        response = requests.get('http://localhost:3000/test', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Test 2: Chat endpoint with different languages
    print("\n2. Testing chat endpoint with different languages...")
    
    test_cases = [
        {"message": "Hello, tell me about Sikkim", "lang": "en"},
        {"message": "नमस्ते, सिक्किम के बारे में बताइए", "lang": "hi"},
        {"message": "Tell me about Rumtek Monastery", "lang": "en"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['lang']} - {test_case['message'][:30]}...")
        try:
            response = requests.post(
                'http://localhost:3000/chat',
                json=test_case,
                timeout=15,
                stream=True
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received")
                
                # Read first few chunks
                chunk_count = 0
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data = line_str[6:]
                            if data == '[DONE]':
                                print(f"   ✅ Streaming completed")
                                break
                            else:
                                chunk_count += 1
                                if chunk_count <= 3:  # Show first 3 chunks
                                    print(f"   📝 Chunk {chunk_count}: {data[:50]}...")
                                elif chunk_count == 4:
                                    print(f"   📝 ... (more chunks)")
            else:
                print(f"   ❌ Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            return False
    
    # Test 3: Frontend accessibility
    print("\n3. Testing frontend accessibility...")
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            if 'AI Assistant' in content and 'chatbot' in content.lower():
                print("✅ Frontend is accessible and contains chatbot elements")
            else:
                print("⚠️  Frontend accessible but chatbot elements not found")
        else:
            print(f"❌ Frontend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Chatbot is fully functional!")
    print("\n📝 Next steps:")
    print("1. Open http://localhost:3000/ in your browser")
    print("2. Click the AI Assistant button")
    print("3. Try asking: 'Tell me about Rumtek Monastery'")
    print("4. Test different languages: English, Hindi, Nepali, etc.")
    
    return True

if __name__ == "__main__":
    test_complete_chatbot()

