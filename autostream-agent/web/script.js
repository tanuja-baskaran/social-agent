const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let sessionId = localStorage.getItem('autostream_session_id') || '';

function generateTime() {
     const now = new Date();
     return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function appendMessage(text, sender) {
     const messageDiv = document.createElement('div');
     messageDiv.classList.add('message', `${sender}-message`);

     const contentDiv = document.createElement('div');
     contentDiv.classList.add('message-content');
     contentDiv.textContent = text;
     // Handle newlines as breaks
     contentDiv.innerHTML = text.replace(/\n/g, '<br>');

     const metaDiv = document.createElement('div');
     metaDiv.classList.add('message-meta');
     metaDiv.textContent = sender === 'user' ? 'You' : 'AutoStream AI';

     messageDiv.appendChild(contentDiv);
     messageDiv.appendChild(metaDiv);

     chatContainer.appendChild(messageDiv);
     scrollToBottom();
}

function scrollToBottom() {
     chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
     const indicator = document.createElement('div');
     indicator.className = 'typing';
     indicator.id = 'typing-indicator';
     indicator.innerHTML = '<span></span><span></span><span></span>';
     chatContainer.appendChild(indicator);
     scrollToBottom();
}

function removeTypingIndicator() {
     const indicator = document.getElementById('typing-indicator');
     if (indicator) indicator.remove();
}

async function sendMessage() {
     const text = userInput.value.trim();
     if (!text) return;

     // Display User Message
     appendMessage(text, 'user');
     userInput.value = '';
     userInput.focus();

     // Show Loading
     showTypingIndicator();

     try {
          const response = await fetch('http://localhost:8000/chat', {
               method: 'POST',
               headers: {
                    'Content-Type': 'application/json',
               },
               body: JSON.stringify({
                    message: text,
                    session_id: sessionId
               })
          });

          const data = await response.json();

          // Save Session ID so context persists on reload
          if (data.session_id) {
               sessionId = data.session_id;
               localStorage.setItem('autostream_session_id', sessionId);
          }

          removeTypingIndicator();
          appendMessage(data.response, 'assistant');

     } catch (error) {
          removeTypingIndicator();
          console.error('Error:', error);
          appendMessage("Sorry, I'm having trouble connecting to the server. Please ensure the agent backend is running.", 'assistant');
     }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
     if (e.key === 'Enter') {
          sendMessage();
     }
});

// Initial focus
userInput.focus();
