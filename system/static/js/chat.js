const openChat = () => {
  document.getElementById("chat-box").style.display = "block";
};

const closeChat = () => {
  document.getElementById("chat-box").style.display = "none";
};

// Chatbot integration
const chatBox = document.getElementById("chat-box");
const inputField = chatBox.querySelector("input[type='text']");
const button = chatBox.querySelector("button");
const chatBoxBody = chatBox.querySelector(".msg_card_body");

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
  const timestamp = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
  chatBoxBody.innerHTML += `
    <div class="msg_container">
      <div class="message msg_cotainer_send">
        <p>${message}</p>
        <span class="msg_time_send">${timestamp}</span>
      </div>
    </div>`;
  chatBoxBody.innerHTML += `
    <div class="msg_container">
      <div id="loading" class="response loading">.</div>
    </div>`;
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
        const botTimestamp = new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });
        chatBoxBody.innerHTML += `
          <div class="msg_container">
            <div class="response msg_cotainer">
              <p>${data.bot}</p>
              <span class="msg_time">${botTimestamp}</span>
            </div>
          </div>`;
      } else {
        chatBoxBody.innerHTML += `
          <div class="msg_container">
            <div class="response error msg_cotainer">
              <p>Unexpected response format.</p>
            </div>
          </div>`;
      }
      scrollToBottom();
    })
    .catch((error) => {
      console.error("Error fetching response:", error);
      document.getElementById("loading").remove();
      chatBoxBody.innerHTML += `
        <div class="msg_container">
          <div class="response error msg_cotainer">
            <p>Failed to fetch response. Please try again later.</p>
          </div>
        </div>`;
      scrollToBottom();
    });
}

function scrollToBottom() {
  chatBoxBody.scrollTop = chatBoxBody.scrollHeight;
}
