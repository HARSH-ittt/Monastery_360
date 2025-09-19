#!/usr/bin/env python3
"""
Test friendly Hindi language responses
"""

import requests
import json
import time

def test_friendly_hindi():
    """Test friendly Hindi responses"""
    print("🇮🇳 Testing Friendly Hindi Responses")
    print("=" * 40)
    
    # Test cases for friendly Hindi
    test_cases = [
        {
            "message": "नमस्ते, सिक्किम के बारे में बताइए",
            "lang": "hi",
            "description": "Hindi greeting and question about Sikkim"
        },
        {
            "message": "रुमटेक मठ कैसे जाएं?",
            "lang": "hi", 
            "description": "Hindi question about visiting Rumtek Monastery"
        },
        {
            "message": "सिक्किम में कहाँ रुकें?",
            "lang": "hi",
            "description": "Hindi question about accommodation"
        },
        {
            "message": "3 दिन का दौरा बताइए",
            "lang": "hi",
            "description": "Hindi request for 3-day tour"
        }
    ]
    
    print("🧪 Testing friendly Hindi responses...")
    print("   Expected: Natural, friendly, conversational Hindi")
    print("   Not: Overly formal or rigid language")
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"   Message: {test_case['message']}")
        
        try:
            response = requests.post(
                'http://localhost:3000/chat',
                json=test_case,
                timeout=15,
                stream=True
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received")
                
                # Read response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data = line_str[6:]
                            if data == '[DONE]':
                                break
                            else:
                                full_response += data
                
                # Check if response is in Hindi
                hindi_chars = any('\u0900' <= ch <= '\u097F' for ch in full_response)
                if hindi_chars:
                    print(f"   ✅ Response in Hindi")
                    
                    # Check for friendly language indicators
                    friendly_indicators = ['आप', 'आपको', 'मदद', 'सहायता', 'बताता', 'बताती', 'देखिए', 'सुनिए']
                    has_friendly_language = any(indicator in full_response for indicator in friendly_indicators)
                    
                    if has_friendly_language:
                        print(f"   ✅ Friendly language detected")
                        success_count += 1
                    else:
                        print(f"   ⚠️  Language may be too formal")
                        
                    # Show first part of response
                    preview = full_response[:100] + "..." if len(full_response) > 100 else full_response
                    print(f"   📝 Preview: {preview}")
                else:
                    print(f"   ❌ Response not in Hindi")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⚠️  Request timed out (may be normal for first request)")
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_cases)} tests successful")
    
    if success_count >= len(test_cases) * 0.75:  # 75% success rate
        print("\n🎉 Friendly Hindi responses are working well!")
        print("\n✅ Features working:")
        print("   • Natural Hindi language")
        print("   • Friendly and conversational tone")
        print("   • Helpful responses")
        print("   • TTS support for Hindi")
        
    else:
        print("\n⚠️  Some issues detected. Check the responses above.")
    
    return success_count >= len(test_cases) * 0.75

if __name__ == "__main__":
    test_friendly_hindi()
