#!/usr/bin/env python3
"""
Simple chat endpoint test
"""

import requests
import json
import time

def test_chat_simple():
    """Test chat endpoint with simple request"""
    print("🔍 Testing chat endpoint...")
    
    try:
        payload = {
            "message": "Hello",
            "lang": "en"
        }
        
        print("📤 Sending request to chat endpoint...")
        print(f"Payload: {payload}")
        
        # Test with shorter timeout first
        response = requests.post(
            'http://localhost:3000/chat',
            json=payload,
            timeout=5
        )
        
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Chat endpoint is working!")
            print("📝 Response content type:", response.headers.get('content-type'))
            
            # Try to read the first few lines of the response
            print("📝 First few lines of response:")
            lines = response.text.split('\n')[:5]
            for i, line in enumerate(lines):
                print(f"  {i+1}: {line}")
            
            return True
        else:
            print(f"❌ Chat endpoint error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Simple Chat Test")
    print("=" * 20)
    
    test_chat_simple()

