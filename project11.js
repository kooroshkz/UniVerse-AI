function sendMessage() {
    const inputBox = document.getElementById('user-input');
    const userInput = inputBox.value.trim();

    if (userInput) {
        displayMessage(userInput, 'user');
        setTimeout(() => {
            const response = generateResponse(userInput); // Simulated bot response
            displayMessage(response, 'bot');
        }, 500); // Delay for bot response
        inputBox.value = ''; // Clear the input field
    }
}

function displayMessage(text, type) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to the latest message
}

function generateResponse(userInput) {
    // Example bot response logic
    if (userInput.toLowerCase().includes("schedule")) {
        return "Your schedule is available on your dashboard.";
    }
    return `You said: "${userInput}"`;
}
