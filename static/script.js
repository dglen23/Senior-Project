// Ensure the button click event is registered once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("sendBtn").addEventListener("click", sendMessage);
});

function sendMessage(event) {
    event.preventDefault(); // Prevent the form from submitting
    const userMessage = document.getElementById("userInput").value;

    if (userMessage.trim() !== "") {
        displayMessage(userMessage, "You"); // Display user message

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            displayMessage(data.reply, "Bot"); // Display bot reply
        })
        .catch((error) => {
            displayMessage("Sorry, there was an error.", "Bot"); // Handle errors
            console.error("Error:", error);
        });

        // Clear input field
        document.getElementById("userInput").value = "";
    }
}

function displayMessage(message, sender) {
    const messagesDiv = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender.toLowerCase());
    messageDiv.textContent = `${sender}: ${message}`;
    messagesDiv.appendChild(messageDiv);

    // Scroll to the bottom of the chatbox
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
