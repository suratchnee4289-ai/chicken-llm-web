document.addEventListener("DOMContentLoaded", () => {
  const messages = document.getElementById("messages");
  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  const API_URL = "/chat";

  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function showTyping() {
    const typing = document.createElement("div");
    typing.className = "message bot typing";
    typing.textContent = "Mom is typing…";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
    return typing;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    sendBtn.disabled = true;

    const typingEl = showTyping();

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();
      typingEl.remove();
      addMessage(data.reply, "bot");

    } catch (err) {
      typingEl.remove();
      addMessage("Mom couldn’t answer right now 🤍", "bot");
      console.error(err);
    } finally {
      sendBtn.disabled = false;
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
