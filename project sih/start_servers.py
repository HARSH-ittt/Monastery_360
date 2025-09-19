#!/usr/bin/env python3
"""
Startup script for the Sikkim Travel Assistant with Mistral AI
This script helps you start the necessary services
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    try:
        # Try to start Ollama in the background
        if sys.platform == "win32":
            subprocess.Popen(['ollama', 'serve'], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for Ollama to start
        print("⏳ Waiting for Ollama to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama_running():
                print("✅ Ollama is now running!")
                return True
            time.sleep(1)
            print(f"   Waiting... ({i+1}/30)")
        
        print("❌ Ollama failed to start within 30 seconds")
        return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first:")
        print("   Visit: https://ollama.ai/download")
        return False
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def check_mistral_model():
    """Check if Mistral model is available"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            mistral_models = [m for m in models if 'mistral' in m.get('name', '').lower()]
            return len(mistral_models) > 0
        return False
    except:
        return False

def download_mistral():
    """Download Mistral model if not available"""
    print("📥 Downloading Mistral model...")
    try:
        # Try to pull the mistral model
        result = subprocess.run(['ollama', 'pull', 'mistral'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Mistral model downloaded successfully!")
            return True
        else:
            print(f"❌ Failed to download Mistral: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Download timed out. Please try manually: ollama pull mistral")
        return False
    except Exception as e:
        print(f"❌ Error downloading Mistral: {e}")
        return False

def start_python_server():
    """Start Python Flask server"""
    print("🐍 Starting Python Flask server...")
    try:
        server_path = Path("backend/api/server.py")
        if server_path.exists():
            subprocess.Popen([sys.executable, str(server_path)], 
                           cwd=Path.cwd())
            print("✅ Python server started on http://localhost:3000")
            return True
        else:
            print("❌ Python server file not found")
            return False
    except Exception as e:
        print(f"❌ Error starting Python server: {e}")
        return False

def start_node_server():
    """Start Node.js server"""
    print("🟢 Starting Node.js server...")
    try:
        server_path = Path("backend/api/server.js")
        if server_path.exists():
            subprocess.Popen(['node', str(server_path)], 
                           cwd=Path.cwd())
            print("✅ Node.js server started on http://localhost:3000")
            return True
        else:
            print("❌ Node.js server file not found")
            return False
    except Exception as e:
        print(f"❌ Error starting Node.js server: {e}")
        return False

def main():
    print("🏔️  Sikkim Travel Assistant with Mistral AI")
    print("=" * 50)
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("🔧 Ollama is not running. Starting it...")
        if not start_ollama():
            print("❌ Cannot start Ollama. Please install it first.")
            return
    else:
        print("✅ Ollama is already running")
    
    # Check if Mistral model is available
    if not check_mistral_model():
        print("📥 Mistral model not found. Downloading...")
        if not download_mistral():
            print("❌ Cannot download Mistral model. Please try manually:")
            print("   ollama pull mistral")
            return
    else:
        print("✅ Mistral model is available")
    
    # Ask user which server to start
    print("\n🤔 Which server would you like to start?")
    print("1. Python Flask server (recommended)")
    print("2. Node.js server")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        start_python_server()
    elif choice == "2":
        start_node_server()
    elif choice == "3":
        start_python_server()
        time.sleep(2)
        start_node_server()
    else:
        print("❌ Invalid choice")
        return
    
    print("\n🎉 Setup complete!")
    print("\n📝 Next steps:")
    print("1. Open frontend/index.html in your browser")
    print("2. Click the AI Assistant button to start chatting")
    print("3. The chatbot is now powered by Mistral AI!")
    
    print("\n🔧 Troubleshooting:")
    print("- If the chatbot doesn't respond, check that Ollama is running")
    print("- Make sure the Mistral model is downloaded: ollama list")
    print("- Check server logs for any errors")

if __name__ == "__main__":
    main()
