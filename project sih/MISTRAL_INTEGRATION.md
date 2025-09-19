# Mistral AI Integration for Sikkim Travel Assistant

## Overview
The Sikkim Travel Assistant chatbot has been successfully integrated with Mistral AI through Ollama. This provides enhanced conversational capabilities for helping users plan their Sikkim monastery tours.

## What's Been Updated

### 1. Backend Servers
- **Python Flask Server** (`backend/api/server.py`):
  - Updated to use `mistral` model instead of `phi3`
  - Optimized parameters for Mistral (temperature: 0.7, top_p: 0.9)
  - Enhanced streaming support
  - Multi-language support maintained (English, Hindi, Nepali, Sikkimese, Lepcha)

- **Node.js Server** (`backend/api/server.js`):
  - Updated to use `mistral` model consistently
  - Added proper Mistral configuration parameters
  - Maintained streaming functionality

### 2. Model Configuration
- **Model**: `mistral` (latest version)
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **Top-p**: 0.9 (good response diversity)
- **Repeat Penalty**: 1.1 (reduces repetition)
- **Context Length**: 4096 tokens
- **Max Predict**: 512 tokens per response

### 3. Frontend
- No changes needed - existing streaming implementation works perfectly with Mistral
- Multi-language support preserved
- Text-to-speech functionality maintained for English responses

## Quick Start

### Prerequisites
1. **Ollama installed**: Download from https://ollama.ai/download
2. **Mistral model downloaded**: `ollama pull mistral`
3. **Python dependencies**: `pip install -r backend/requirements.txt`
4. **Node.js dependencies**: `npm install` (if using Node.js server)

### Running the Application

#### Option 1: Automated Setup
```bash
python start_servers.py
```

#### Option 2: Manual Setup
1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Start Backend Server** (choose one):
   ```bash
   # Python Flask server
   python backend/api/server.py
   
   # OR Node.js server
   node backend/api/server.js
   ```

3. **Open Frontend**:
   - Open `frontend/index.html` in your browser
   - Click the AI Assistant button to start chatting

### Testing the Integration
```bash
python test_mistral_integration.py
```

## Features

### Multi-Language Support
- **English**: Default language for international visitors
- **Hindi**: For Hindi-speaking travelers
- **Nepali**: For visitors from Nepal
- **Sikkimese**: For local cultural insights
- **Lepcha**: For indigenous heritage exploration

### AI Capabilities
- **Tour Planning**: Customized monastery tour itineraries
- **Accommodation Recommendations**: Local lodging suggestions
- **Cultural Insights**: Information about Sikkim's heritage
- **Travel Tips**: Practical advice for visitors
- **Real-time Streaming**: Fast, responsive conversations

### Technical Features
- **Streaming Responses**: Real-time text generation
- **Text-to-Speech**: Audio responses for English (optional)
- **Error Handling**: Graceful fallbacks and error messages
- **Mobile Responsive**: Works on all device sizes

## Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama"**
   - Ensure Ollama is running: `ollama serve`
   - Check if port 11434 is available

2. **"Mistral model not found"**
   - Download the model: `ollama pull mistral`
   - Verify with: `ollama list`

3. **"Failed to connect to AI server"**
   - Check if backend server is running on port 3000
   - Verify no other application is using port 3000

4. **Slow responses**
   - Mistral is a large model - first response may be slower
   - Consider using a smaller model like `mistral:7b` for faster responses

### Performance Tips

1. **For faster responses**:
   ```bash
   ollama pull mistral:7b  # Smaller, faster model
   ```
   Then update the model name in server files to `mistral:7b`

2. **For better quality**:
   - Use the full `mistral` model (current default)
   - Increase `num_ctx` for longer conversations

3. **Memory optimization**:
   - Close other applications to free up RAM
   - Mistral requires significant memory (8GB+ recommended)

## API Endpoints

### Python Flask Server
- `POST /chat` - Main chat endpoint with language support
- `GET /chat-stream` - Alternative streaming endpoint

### Node.js Server
- `POST /chat` - Streaming chat endpoint

### Request Format
```json
{
  "message": "Tell me about Rumtek Monastery",
  "lang": "en"  // auto, en, hi, ne, si, lep
}
```

### Response Format
Server-Sent Events (SSE) with streaming text:
```
data: Response text chunk
data: [DONE]
```

## Development

### Adding New Languages
1. Update language detection in `server.py`
2. Add system instructions for the new language
3. Update frontend language selector

### Customizing Responses
1. Modify system instructions in `server.py`
2. Adjust model parameters (temperature, top_p, etc.)
3. Test with different prompts

### Monitoring
- Check server logs for errors
- Monitor Ollama logs: `ollama logs`
- Use browser developer tools for frontend debugging

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Run the test script: `python test_mistral_integration.py`
3. Verify Ollama is working: `ollama list` and `ollama run mistral`

---

**Status**: ✅ Fully Integrated and Tested
**Last Updated**: January 2025
**Mistral Model**: mistral:latest
