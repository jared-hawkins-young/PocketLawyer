/* document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat');
  
    sendBtn.addEventListener('click', function () {
      const userText = userInput.value;
      if (userText.trim()) {
        postMessage(userText);
        userInput.value = '';
        appendMessage('You', userText);
      }
    });
  
    // Allow the user to press enter to send a message
    userInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        sendBtn.click();
      }
    });
  
    function postMessage(message) {
      fetch('/ask', {
        method: 'POST',
        body: new URLSearchParams({ 'message': message }),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      .then(response => response.json())
      .then(data => {
        appendMessage('Bot', data.response);
      })
      .catch(error => {
        console.error('Error:', error);
        appendMessage('Bot', 'Sorry, there was an error processing your request.');
      });
    }
  
    function appendMessage(sender, message) {
      const messageElem = document.createElement('li');
      messageElem.innerHTML = `<strong>${sender}:</strong> ${message}`;
      chatBox.appendChild(messageElem);
      // Auto scroll to the bottom of the chat box
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
  */

  // script.js
  document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.querySelector('#chat-container button');

    sendButton.addEventListener('click', function() {
        sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat("You: " + message, 'user-message');
            userInput.value = '';
            sendMessageToServer(message);
        }
    }

    function addMessageToChat(message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.className = className;
        chatBox.appendChild(messageDiv);
    }

    function sendMessageToServer(message) {
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat("Bot: " + data.message, 'bot-message');
        })
        .catch(error => console.error('Error:', error));
    }
});
