// Keep track of chats and their history
let chats = [];
let currentChatId = null;

function createNewChat() {
    // Create a unique chat ID (you may want to generate this dynamically)
    let chatname = prompt("Please enter chat name:")
    if (chatname == null || chatname == "") {
        chatname = "New Chat";
    }
    const chatId = Date.now().toString();

    // Create a new chat object
    const newChat = {
        name: chatname,
        id: chatId,
        history: []
    };

    // Add the chat to the list of chats
    chats.push(newChat);

    // Update the chat list in the sidebar
    updateChatList();

    // Set the current chat to the new chat
    setCurrentChat(chatId);
}

function createLoadedNewChat(chatname, chatId, history) {
    // Create a unique chat ID (you may want to generate this dynamically)

    // Create a new chat object
    const newChat = {
        name: chatname + '(READ ONLY)',
        id: chatId,
        history: history
    };

    // Add the chat to the list of chats
    chats.push(newChat);

    // Update the chat list in the sidebar
    updateChatList();

    // Set the current chat to the new chat
    setCurrentChat(chatId);
}

function setCurrentChat(chatId) {
    // Retrieve the chat element
    const chatElement = document.getElementById('chat');

    // Find the chat object based on the chatId
    const currentChat = chats.find(chat => chat.id == chatId);


    // Display the chat history in the chat element
    chatElement.innerHTML = currentChat.history.join('<br>');

    // Update the currently selected chat ID
    currentChatId = chatId;

    // Highlight the clicked chat
    highlightChat(chatId);
}

function sendMessage() {
    const userMessageInput = document.getElementById('user-message');
    const message = userMessageInput.value;

    if (message.trim() !== '') {
        // Get the current chat
        const currentChat = getCurrentChat();

        // Add the message to the chat history
        currentChat.history.push('user: ' + message);

        // Update the chat display
        setCurrentChat(currentChat.id);

        // Clear the input field
        userMessageInput.value = '';

        // Get the bot response
        get_response();
    }
}

function history_string(){
    // Get the current chat
    const currentChat = getCurrentChat();
    //get the history
    const history = currentChat.history;
    //retunr the history as a string
    return history.join('-__-');
}

function get_response(){
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'history=' + history_string(),
        
    })
    .then(response => response.json())
    .then(data => {
        // Get the current chat
        const currentChat = getCurrentChat();

        // Add the message to the chat history
        currentChat.history.push('bot: ' + data.bot_response);

        // Update the chat display
        setCurrentChat(currentChat.id);
        saveChat();
    })
    

}

function updateChatList() {
    // Retrieve the chat list element
    const chatListElement = document.getElementById('chat-list');

    // Update the chat list with the names of all chats
    chatListElement.innerHTML = chats.map(chat => `<div onclick="setCurrentChat('${chat.id}')" class="chat-session">${chat.name}</div>`).join('');
    
}

function getCurrentChat() {
    // You might want to keep track of the current chat ID separately
    return currentChatId ? chats.find(chat => chat.id === currentChatId) : null;
    
}

function highlightChat(chatId) {
    // Remove the "active" class from all chat items
    const chatItems = document.querySelectorAll('.chat-session');
    chatItems.forEach(item => item.classList.remove('selected'));

    // Add the "active" class to the clicked chat item
    const activeChatItem = document.querySelector(`.chat-session[data-chat-id="${chatId}"]`);
    if (activeChatItem) {
        activeChatItem.classList.add('selected');
    }
}

function saveChat() {

    //loop through all chats
    for (let i = 0; i < chats.length; i++) {
        //get the chat
        const chat = chats[i];
        //get the chat history
        const history = chat.history.join('-__-');
        //get the chat name
        const name = chat.name;
        //get the chat id
        const id = chat.id;
        //save the chat to the database
        save_chat(id, name, history);
    }

}

function save_chat(id, name, history){

    fetch('/save_chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'id=' + id + '&name=' + name + '&history=' + history,
        
    })
}


function deleteChat() {
    // Remove the current chat from the list of chats
    chats = chats.filter(chat => chat.id !== currentChatId);

    // Update the chat list in the sidebar
    updateChatList();

    // Set the current chat to the first chat in the list
    setCurrentChat(chats[0].id);
}

function loadChat() {
    fetch('/load_chat', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        chat = data.chats;
        for (let i = 0; i < chat.length; i++) {
            const Chat = chat[i];
            console.log(Chat.messages);
            createLoadedNewChat(Chat.name, Chat.id, Chat.messages.split('-__-'));
            console.log(i);
        }
    });
}



// Create a new chat when the page loads
loadChat();


//load the chats from the database

