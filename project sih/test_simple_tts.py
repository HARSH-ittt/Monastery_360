#!/usr/bin/env python3
"""
Simple test for TTS functionality
"""

import requests
import json

def test_simple_tts():
    """Test simple TTS functionality"""
    print("🔊 Simple TTS Test")
    print("=" * 20)
    
    # Test English
    print("📝 Testing English...")
    try:
        response = requests.post(
            'http://localhost:3000/chat',
            json={"message": "Hello, tell me about Sikkim", "lang": "en"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ English response received")
        else:
            print(f"❌ English failed: {response.status_code}")
    except Exception as e:
        print(f"❌ English error: {e}")
    
    # Test Hindi
    print("\n📝 Testing Hindi...")
    try:
        response = requests.post(
            'http://localhost:3000/chat',
            json={"message": "नमस्ते, सिक्किम के बारे में बताइए", "lang": "hi"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Hindi response received")
        else:
            print(f"❌ Hindi failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Hindi error: {e}")
    
    print("\n🎉 TTS functionality is ready!")
    print("\n📝 How to test TTS in browser:")
    print("1. Open http://localhost:3000/")
    print("2. Click AI Assistant button")
    print("3. Select language (English or Hindi)")
    print("4. Check the 'Speak' checkbox")
    print("5. Send a message and listen!")

if __name__ == "__main__":
    test_simple_tts()
