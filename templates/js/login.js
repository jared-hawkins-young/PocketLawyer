function validateLogin() {
    const dummyUsername = "username";
    const dummyPassword = "password";
    
    const enteredUsername = document.getElementById("username").value;
    const enteredPassword = document.getElementById("password").value;
    
    if (enteredUsername === dummyUsername && enteredPassword === dummyPassword) {
        window.location.href = "chatbot.html"
    } else {
        alert("Invalid username or password. Please try again.");
    }
    
    return false;
}