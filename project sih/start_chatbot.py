#!/usr/bin/env python3
"""
Startup script for the Sikkim Chatbot
This script ensures all services are running properly
"""

import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama"""
    print("🚀 Starting Ollama...")
    try:
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Wait for Ollama to start
        for i in range(30):
            if check_ollama():
                print("✅ Ollama started successfully")
                return True
            time.sleep(1)
            print(f"   Waiting for Ollama... ({i+1}/30)")
        print("❌ Ollama failed to start")
        return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install it first:")
        print("   Visit: https://ollama.ai/download")
        return False

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
        subprocess.Popen([sys.executable, 'backend/api/server.py'], cwd=Path.cwd())
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
            timeout=10,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Chat functionality working")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def main():
    print("🏔️  Sikkim Chatbot Startup")
    print("=" * 40)
    
    # Check Ollama
    if not check_ollama():
        if not start_ollama():
            return False
    else:
        print("✅ Ollama is already running")
    
    # Check server
    if not check_server():
        if not start_server():
            return False
    else:
        print("✅ Python server is already running")
    
    # Test chat
    if not test_chat():
        print("❌ Chat functionality test failed")
        return False
    
    print("\n🎉 All services are running!")
    print("\n📝 Next steps:")
    print("1. Open frontend/index.html in your browser")
    print("2. Or open test_chatbot_frontend.html for a simple test")
    print("3. Click the AI Assistant button to start chatting")
    
    # Ask if user wants to open browser
    try:
        choice = input("\nWould you like to open the test page in your browser? (y/n): ").lower()
        if choice in ['y', 'yes']:
            webbrowser.open('test_chatbot_frontend.html')
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    return True

if __name__ == "__main__":
    main()

