'use strict';

var chatSessions = [];
var currentChat = [];
var chatCount = 0; 
var autoSelectNewChat = true;

var userStartedNewChat = false;

function sendMessage() {
    var userMessage = document.getElementById('user-message').value;
    document.getElementById('user-message').value = '';
    if (userMessage.trim() === '') {
        return;
    }
    processMessage(userMessage);
}

function processMessage(userMessage) {
    var chatContainer = document.getElementById('chat');

    var userDiv = document.createElement('div');
    userDiv.className = 'user-message';
    userDiv.innerHTML = '<strong>You:</strong> ' + userMessage;

    chatContainer.appendChild(userDiv);
    currentChat.push({ type: 'user', message: userMessage });

    if (!userStartedNewChat) {
        if (currentChat.length > 0) {
            chatSessions.push({ id: ++chatCount, messages: currentChat });
        }
        currentChat = [];
        updateSidebar();
        userStartedNewChat = true;
    }

    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_message=' + encodeURIComponent(userMessage),
    })
    .then(response => response.json())
    .then(data => {
        var botDiv = document.createElement('div');
        botDiv.className = 'bot-message';
        botDiv.innerHTML = '<strong>Bot:</strong> ' + data.bot_response.replace('You said:', '');
        chatContainer.appendChild(botDiv);
        currentChat.push({ type: 'bot', message: data.bot_response });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateSidebar() {
    var chatHistoryContainer = document.getElementById('chat-history');
    chatHistoryContainer.innerHTML = '';

    var newChatButton = document.getElementById('new-chat-button');
    newChatButton.disabled = chatSessions.length === 0;

    chatSessions.forEach(session => {
        var sessionDiv = document.createElement('div');
        sessionDiv.className = 'chat-session';
        sessionDiv.setAttribute('data-chat-id', session.id);
        sessionDiv.innerHTML = 'Chat Session ' + session.id;
        sessionDiv.addEventListener('click', function () {
            document.querySelectorAll('.chat-session').forEach(element => {
                element.classList.remove('selected');
            });
            sessionDiv.classList.add('selected');
            loadChatSession(session);
        });
        chatHistoryContainer.appendChild(sessionDiv);
    });

    if (chatSessions.length > 0) {
        document.querySelector('.chat-session').classList.add('selected');
        loadChatSession(chatSessions[0]);
    }
}

function loadChatSession(session) {
    currentChat = [];
    document.getElementById('chat').innerHTML = '';

    session.messages.forEach(message => {
        var messageDiv = document.createElement('div');
        messageDiv.className = message.type + '-message';
        messageDiv.innerHTML = '<strong>' + message.type.charAt(0).toUpperCase() + message.type.slice(1) + ':</strong> ' + message.message;
        document.getElementById('chat').appendChild(messageDiv);
        currentChat.push(message);
    });

    document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
    userStartedNewChat = false;
}

document.getElementById('user-message').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('new-chat-button').addEventListener('click', function () {
    startNewChat();
    updateSidebar();
});

function startNewChat() {
    if (userStartedNewChat) {
        chatSessions.push({ id: ++chatCount, messages: [...currentChat] });
        updateSidebar();
        currentChat = [];
    }

    var newChatButton = document.getElementById('new-chat-button');
    newChatButton.disabled = false;  
    var newChatId = chatCount;
    selectChatSession(newChatId);

    userStartedNewChat = true;
    var selectedChat = document.querySelector('.chat-session.selected');
    if (selectedChat) {
        document.getElementById('chat').innerHTML = '';
    }
    document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
}

document.getElementById('new-chat-button').addEventListener('click', function () {
    startNewChat();
});

function selectChatSession(chatId) {
    var chatSession = document.querySelector('.chat-session.selected');
    if (chatSession) {
        chatSession.classList.remove('selected');
    }

    var selectedChat = document.querySelector('.chat-session[data-chat-id="' + chatId + '"]');
    if (selectedChat) {
        selectedChat.classList.add('selected');
        loadChatSession(chatSessions.find(session => session.id === chatId));
    }
}
updateSidebar();