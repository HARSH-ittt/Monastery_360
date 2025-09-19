// Chatbot Widget Implementation
document.addEventListener('DOMContentLoaded', function() {
    // Create chatbot widget elements
    const chatWidget = document.createElement('div');
    chatWidget.className = 'chat-widget';
    chatWidget.innerHTML = `
        <div class="chat-button">
            <i class="fas fa-robot"></i>
        </div>
        <div class="chat-popup">
            <div class="chat-header">
                <h3>Sikkim Tourism Assistant</h3>
                <button class="close-chat"><i class="fas fa-times"></i></button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message ai-message">
                    <strong>AI:</strong> Hello! I'm your Sikkim Tourism Assistant. Ask me about monasteries, food, or festivals!
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="userMessage" placeholder="Type your question here..." />
                <button id="sendMessage"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    `;
    
    document.body.appendChild(chatWidget);
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            font-family: 'Inter', sans-serif;
        }
        
        .chat-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--gradient-primary);
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .chat-button:hover {
            transform: scale(1.1);
        }
        
        .chat-button i {
            color: white;
            font-size: 24px;
        }
        
        .chat-popup {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 30px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            display: none;
            transition: all 0.3s ease;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .chat-popup.active {
            display: flex;
            flex-direction: column;
            animation: popIn 0.3s forwards;
        }
        
        @keyframes popIn {
            0% { opacity: 0; transform: translateY(20px) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .chat-header {
            background: var(--gradient-primary);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .chat-header h3 {
            margin: 0;
            font-size: 16px;
        }
        
        .close-chat {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 16px;
        }
        
        .chat-messages {
            height: 300px;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: #f9f9f9;
        }
        
        .message {
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
            word-break: break-word;
        }
        
        .user-message {
            background: #e3f2fd;
            color: #0d47a1;
            align-self: flex-end;
        }
        
        .ai-message {
            background: #f1f1f1;
            color: #333;
            align-self: flex-start;
        }
        
        .chat-input {
            display: flex;
            padding: 10px;
            border-top: 1px solid #eee;
        }
        
        .chat-input input {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
        }
        
        .chat-input button {
            background: var(--gradient-primary);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            margin-left: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .chat-input button:hover {
            transform: scale(1.1);
        }
    `;
    
    document.head.appendChild(style);
    
    // Add event listeners
    const chatButton = document.querySelector('.chat-button');
    const chatPopup = document.querySelector('.chat-popup');
    const closeChat = document.querySelector('.close-chat');
    const sendButton = document.getElementById('sendMessage');
    const userInput = document.getElementById('userMessage');
    
    chatButton.addEventListener('click', function() {
        chatPopup.classList.toggle('active');
    });
    
    closeChat.addEventListener('click', function() {
        chatPopup.classList.remove('active');
    });
    
    sendButton.addEventListener('click', sendUserMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendUserMessage();
        }
    });
    
    function sendUserMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        // Send message to server
        fetch('http://localhost:3000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                lang: 'en'
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.response) {
                // Add AI response to chat
                addMessage(data.response, false);
            } else {
                throw new Error('Invalid response format');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again.', false);
        });
    }
    
    function addMessage(text, isUser) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'AI'}:</strong> ${text}`;
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});