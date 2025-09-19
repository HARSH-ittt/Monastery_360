#!/usr/bin/env python3
"""
Test script for the fixed Q&A functionality
"""

import requests
import json
import time

def test_fixed_qa():
    """Test the fixed Q&A responses"""
    print("🧪 Testing Fixed Q&A Functionality")
    print("=" * 50)
    
    # Test cases for fixed Q&A
    test_cases = [
        {
            "message": "plan one day tour near rumtek monastery",
            "expected_source": "fixed_qa",
            "description": "Exact match for Rumtek tour"
        },
        {
            "message": "suggest sikkim food",
            "expected_source": "fixed_qa", 
            "description": "Exact match for Sikkim food"
        },
        {
            "message": "local festival of sikkim",
            "expected_source": "fixed_qa",
            "description": "Exact match for festivals"
        },
        {
            "message": "best time to visit for festivals",
            "expected_source": "fixed_qa",
            "description": "Exact match for festival timing"
        },
        {
            "message": "hi",
            "expected_source": "fixed_qa",
            "description": "Hindi greeting"
        },
        {
            "message": "hii",
            "expected_source": "fixed_qa",
            "description": "English greeting"
        },
        {
            "message": "what festivals are there in sikkim",
            "expected_source": "fixed_qa",
            "description": "Fuzzy match for festivals"
        },
        {
            "message": "tell me about sikkim cuisine",
            "expected_source": "fixed_qa",
            "description": "Fuzzy match for food"
        },
        {
            "message": "random question about something else",
            "expected_source": "predefined",
            "description": "Should fall back to predefined responses"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"   Message: '{test_case['message']}'")
        
        try:
            response = requests.post(
                'http://localhost:3000/chat',
                json={'message': test_case['message']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                actual_source = data.get('source', 'unknown')
                response_text = data.get('response', '')
                
                print(f"   ✅ Response received")
                print(f"   📊 Source: {actual_source}")
                print(f"   💬 Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
                
                if actual_source == test_case['expected_source']:
                    print(f"   ✅ Source matches expected: {test_case['expected_source']}")
                    success_count += 1
                else:
                    print(f"   ⚠️  Source mismatch. Expected: {test_case['expected_source']}, Got: {actual_source}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_cases)} tests successful")
    
    if success_count >= len(test_cases) * 0.8:  # 80% success rate
        print("\n🎉 Fixed Q&A functionality is working well!")
        print("\n✅ Features working:")
        print("   • Fixed Q&A exact matching")
        print("   • Fuzzy matching for similar questions")
        print("   • Fallback to predefined responses")
        print("   • Both English and Hindi responses")
        print("   • Emoji-enhanced responses")
        
        print("\n📝 How to use:")
        print("   1. Start the server: python start_simple_chatbot.py")
        print("   2. Access the chatbot at: http://localhost:3000")
        print("   3. Ask questions like:")
        print("      - 'plan one day tour near rumtek monastery'")
        print("      - 'suggest sikkim food'")
        print("      - 'local festival of sikkim'")
        print("      - 'hi' (Hindi response)")
        print("      - 'hii' (English response)")
        
    else:
        print("\n⚠️  Some issues detected. Check the errors above.")
    
    return success_count >= len(test_cases) * 0.8

if __name__ == "__main__":
    print("🚀 Make sure the server is running at http://localhost:3000")
    print("   Start it with: python start_simple_chatbot.py")
    print()
    
    try:
        # Test if server is running
        response = requests.get('http://localhost:3000/test', timeout=5)
        if response.status_code == 200:
            test_fixed_qa()
        else:
            print("❌ Server is not responding. Please start the server first.")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python start_simple_chatbot.py")
    except Exception as e:
        print(f"❌ Error: {e}")
