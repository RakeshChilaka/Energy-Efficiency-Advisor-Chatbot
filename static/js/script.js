function displayMessage(message, sender) {
    const chatbox = document.getElementById("chatbox");

    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + sender;

    const avatar = document.createElement("img");
    avatar.className = "avatar";
    avatar.src = sender === "bot" ? "/static/images/bot.jpg" : "/static/images/guy.jpg";
    messageDiv.appendChild(avatar);

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.innerText = message;
    messageDiv.appendChild(messageContent);

    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function displayOptions(options) {
    removeOptions();

    const chatbox = document.getElementById("chatbox");
    const optionContainer = document.createElement("div");
    optionContainer.className = "button-group";

    options.forEach(option => {
        const button = document.createElement("button");
        button.className = "button-option";
        button.innerText = option;
        button.onclick = function () {
            removeOptions();
            document.getElementById("userInput").value = option;
            sendMessage();
        };
        optionContainer.appendChild(button);
    });

    chatbox.appendChild(optionContainer);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function removeOptions() {
    document.querySelectorAll(".button-option, .button-group").forEach(el => el.remove());
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();
    if (userInput === "") return;

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

        if (data.show_appliance_options) {
            displayOptions(["Air Conditioner", "Refrigerator", "Fan", "Television", "Lights"]);
        }
    });
}

function checkEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
