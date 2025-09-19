#!/usr/bin/env python3
"""
Simplified startup script for the Sikkim Chatbot
This script ensures all services are running properly
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_server():
    """Check if Python server is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start Python server"""
    print("🚀 Starting Python server...")
    try:
        subprocess.Popen([sys.executable, 'backend/api/simple_server.py'], cwd=Path.cwd())
        # Wait for server to start
        for i in range(10):
            if check_server():
                print("✅ Python server started successfully")
                return True
            time.sleep(1)
            print(f"   Waiting for server... ({i+1}/10)")
        print("❌ Python server failed to start")
        return False
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def test_chat():
    """Test the chat functionality"""
    print("🧪 Testing chat functionality...")
    try:
        response = requests.post(
            'http://localhost:3000/chat',
            json={'message': 'Hello', 'lang': 'en'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Chat functionality working")
            print(f"Response: {response.json().get('response')}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def main():
    print("🏔️  Sikkim Simple Chatbot Startup")
    print("=" * 40)
    
    # Check server
    if not check_server():
        if not start_server():
            return False
    else:
        print("✅ Python server is already running")
    
    # Test chat functionality
    chat_success = test_chat()
    
    if chat_success:
        print("✅ Chatbot is working correctly!")
        print("🌐 You can access the chatbot at: http://localhost:3000")
    else:
        print("❌ Chat functionality test failed")
    
    return chat_success

if __name__ == "__main__":
    main()