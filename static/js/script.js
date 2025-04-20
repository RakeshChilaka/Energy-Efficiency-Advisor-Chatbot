function displayMessage(message, sender) {
    const chatbox = document.getElementById("chatbox");
    
    // Create message container
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + sender;

    // Add avatar based on sender
    const avatar = document.createElement("img");
    avatar.className = "avatar";
    avatar.src = sender === "bot" ? "/static/images/bot.jpg" : "/static/images/guy.jpg"; // Use respective image paths
    messageDiv.appendChild(avatar);

    // Add message content
    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.innerText = message;
    messageDiv.appendChild(messageContent);

    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}


function displayOptions(options) {
    const chatbox = document.getElementById("chatbox");
    // Clear previous options
    const existingOptions = document.querySelectorAll(".button-option");
    existingOptions.forEach(option => option.remove());

    options.forEach(option => {
        const button = document.createElement("button");
        button.className = "button-option";
        button.innerText = option;
        button.onclick = function() {
            document.getElementById("userInput").value = option;
            sendMessage();
        };
        chatbox.appendChild(button);
    });
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;
    displayMessage(userInput, "user");
    document.getElementById("userInput").value = "";

    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response, "bot");

        // Check if bot response asks for appliance selection
        if (data.response.includes("Which appliance")) {
            displayOptions(["Air Conditioner", "Refrigerator","Fan","Television","Lights"]);
        }
    });
}

function checkEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
