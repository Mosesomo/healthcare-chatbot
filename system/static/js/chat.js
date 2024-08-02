const openChat = () => {
  document.getElementById("chat-box").style.display = "block";
};

const closeChat = () => {
  document.getElementById("chat-box").style.display = "none";
};

// Chatbot integration
const chatBox = document.querySelector(".chat-box");
const inputField = chatBox.querySelector("input[type='text']");
const button = chatBox.querySelector("button");
const chatBoxBody = chatBox.querySelector(".chat-box-body");

button.addEventListener("click", sendMessage);
inputField.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

function sendMessage() {
  const message = inputField.value;
  if (!message.trim()) return; // Avoid sending empty messages
  inputField.value = "";
  chatBoxBody.innerHTML += `<div class="message"><p>${message}</p></div>`;
  chatBoxBody.innerHTML += `<div id="loading" class="response loading">.</div>`;
  scrollToBottom();
  window.dotsGoingUp = true;
  const dots = window.setInterval(function () {
    const wait = document.getElementById("loading");
    if (window.dotsGoingUp) wait.innerHTML += ".";
    else {
      wait.innerHTML = wait.innerHTML.substring(1);
      if (wait.innerHTML.length < 2) window.dotsGoingUp = true;
    }
    if (wait.innerHTML.length > 3) window.dotsGoingUp = false;
  }, 250);

  fetch("https://bot-red-sigma.vercel.app/chat", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userInput: message }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("loading").remove();
      console.log("API Response:", data); // Log the API response
      if (data.bot) {
        chatBoxBody.innerHTML += `<div class="response"><p>${data.bot}</p></div>`;
      } else {
        chatBoxBody.innerHTML += `<div class="response error"><p>Unexpected response format.</p></div>`;
      }
      scrollToBottom();
    })
    .catch((error) => {
      console.error("Error fetching response:", error);
      document.getElementById("loading").remove();
      chatBoxBody.innerHTML += `<div class="response error"><p>Failed to fetch response. Please try again later.</p></div>`;
      scrollToBottom();
    });
}

function scrollToBottom() {
  chatBoxBody.scrollTop = chatBoxBody.scrollHeight;
}
