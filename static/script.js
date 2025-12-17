document.addEventListener("DOMContentLoaded", () => {

  const messagesContainer = document.getElementById("messages");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  if (!messagesContainer || !userInput || !sendBtn) {
    console.log("Missing elements", { messagesContainer, userInput, sendBtn });
    return;
  }

  const API_URL = "/chat";

  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    userInput.value = "";
    sendBtn.disabled = true;

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      console.log("reply:", data);
      // addMessage(data.reply, "bot"); ← ถ้าเปิดใช้ UI
    } catch (e) {
      console.log("fetch error:", e);
    } finally {
      sendBtn.disabled = false;
    }
  }

  // ✅ Click
  sendBtn.addEventListener("click", sendMessage);

  // ✅ Enter (ใช้ keydown)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

});
