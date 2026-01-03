const fileInput = document.getElementById("file-input");
const userInput = document.getElementById("user-input");

fileInput.addEventListener("change", uploadFile);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Optimistic UI update
  appendUserMessage(message);
  userInput.value = "";
  userInput.focus();

  // Show typing indicator
  showTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: message })
    });

    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();
    removeTyping();

    const formatted = formatResponse(data);
    appendBotMessage(formatted.text, formatted.agent);

  } catch (error) {
    removeTyping();
    appendBotMessage("❌ Sorry, something went wrong. Please try again.", "System");
    console.error("Error:", error);
  }
}

async function uploadFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Show status
  appendBotMessage(`Uploading **${file.name}**...`, "System");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/document/upload", {
      method: "POST",
      body: formData
    });
    
    const data = await response.json();
    appendBotMessage(data.response, "Document Agent");
  } catch (error) {
    appendBotMessage("❌ File upload failed.", "System");
  }
  
  // Reset input
  fileInput.value = "";
}

function appendUserMessage(text) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "message user-message";
  div.textContent = text;
  chatBox.appendChild(div);
  scrollToBottom();
}

function appendBotMessage(text, agent) {
  const chatBox = document.getElementById("chat-box");
  
  const div = document.createElement("div");
  div.className = "message bot-message";

  const badge = document.createElement("div");
  badge.className = "badge";
  badge.textContent = agent || "Bot";
  
  const content = document.createElement("div");
  content.innerHTML = formatText(text); // Simple formatting

  div.appendChild(badge);
  div.appendChild(content);

  chatBox.appendChild(div);
  scrollToBottom();
}

function showTyping() {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "typing-indicator";
  div.id = "typing";
  div.innerHTML = `
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  `;
  chatBox.appendChild(div);
  scrollToBottom();
}

function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

function scrollToBottom() {
  const chatBox = document.getElementById("chat-box");
  chatBox.scrollTop = chatBox.scrollHeight;
}

function formatResponse(data) {
  let text = "";
  let agent = "System";

  if (data.response) {
      if (typeof data.response === "string") {
          text = data.response;
          agent = (data.agent || "System") + " Agent";
      } else if (typeof data.response === "object") {
           // Handle specific structured responses if needed
           if (data.response.description && data.response.temperature) {
               text = `🌤 **${data.response.description}** with a temperature of **${data.response.temperature}°C**.`;
               agent = "Weather Agent";
           } else {
               text = "<pre>" + JSON.stringify(data.response, null, 2) + "</pre>";
               agent = (data.agent || "Bot") + " Agent";
           }
      }
  } else {
      text = "No response received.";
  }

  // Capitalize Agent Name
  agent = agent.replace(/\b\w/g, c => c.toUpperCase());

  return { text, agent };
}

// Simple Markdown-like formatter for bolding
function formatText(text) {
  // Bold: **text**
  let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Newlines to <br>
  formatted = formatted.replace(/\n/g, '<br>');
  return formatted;
}
