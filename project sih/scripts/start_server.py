#!/usr/bin/env python3
"""
Startup script for Sacred Sikkim AI Chat Application
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_ollama():
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def install_requirements():
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def start_flask_server():
    print("🚀 Starting Flask server...")
    try:
        subprocess.Popen([sys.executable, 'server.py'])
        print("✅ Flask server started on http://localhost:3000")
        return True
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
        return False

def main():
    print("🏔️ Sacred Sikkim AI Chat Application")
    print("=" * 40)

    if not Path('server.py').exists():
        print("❌ server.py not found. Please run this script from the project directory.")
        return

    if not install_requirements():
        return

    print("🔍 Checking Ollama connection...")
    if not check_ollama():
        print("⚠️  Warning: Ollama doesn't seem to be running.")
        print("   Please make sure Ollama is installed and running with the 'phi3' model.")
        print("   You can start Ollama with: ollama serve")
        print("   And pull the phi3 model with: ollama pull phi3")
        print()

    if start_flask_server():
        print()
        print("🎉 Application started successfully!")
        print("📱 Open your browser and go to: http://localhost:3000")
        print("🌐 Or open the index.html file directly in your browser")
        print()
        print("💡 Tips:")
        print("   - Make sure Ollama is running with the 'phi3' model")
        print("   - The AI chat will work when both servers are running")
        print("   - Press Ctrl+C to stop the Flask server")

        time.sleep(2)
        try:
            webbrowser.open('http://localhost:3000/')
        except:
            print("   Please manually open http://localhost:3000/ in your browser")

    print("\n🛑 Press Ctrl+C to stop the server")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
