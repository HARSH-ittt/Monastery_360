#!/usr/bin/env python3
"""
Test Hindi language functionality
"""

import requests
import json
import time

def test_hindi_chat():
    """Test Hindi chat functionality"""
    print("🔍 Testing Hindi language functionality...")
    
    test_cases = [
        {
            "message": "नमस्ते, सिक्किम के बारे में बताइए",
            "lang": "hi",
            "description": "Hindi greeting and question about Sikkim"
        },
        {
            "message": "रुमटेक मठ के बारे में जानकारी दीजिए",
            "lang": "hi", 
            "description": "Hindi question about Rumtek Monastery"
        },
        {
            "message": "Hello, tell me about Sikkim",
            "lang": "en",
            "description": "English question for comparison"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"   Message: {test_case['message']}")
        print(f"   Language: {test_case['lang']}")
        
        try:
            response = requests.post(
                'http://localhost:3000/chat',
                json=test_case,
                timeout=20,
                stream=True
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received (Status: {response.status_code})")
                
                # Read response chunks
                chunk_count = 0
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data = line_str[6:]
                            if data == '[DONE]':
                                print(f"   ✅ Streaming completed")
                                break
                            else:
                                full_response += data
                                chunk_count += 1
                                if chunk_count <= 3:  # Show first 3 chunks
                                    print(f"   📝 Chunk {chunk_count}: {data[:50]}...")
                                elif chunk_count == 4:
                                    print(f"   📝 ... (more chunks)")
                
                # Check if response is in expected language
                if test_case['lang'] == 'hi':
                    # Check for Hindi characters
                    hindi_chars = any('\u0900' <= ch <= '\u097F' for ch in full_response)
                    if hindi_chars:
                        print(f"   ✅ Response contains Hindi text")
                    else:
                        print(f"   ⚠️  Response may not be in Hindi")
                else:
                    print(f"   ✅ English response received")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Request timed out")
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n🎉 Hindi language testing completed!")

if __name__ == "__main__":
    print("🧪 Hindi Language Test")
    print("=" * 30)
    test_hindi_chat()

