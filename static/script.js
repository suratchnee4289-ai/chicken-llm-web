// URL Backend
const API_BASE = "https://chicken-llm-web.onrender.com";

// ส่งข้อความไปยัง Chat API
async function sendMessage() {
    const input = document.getElementById("messageInput");
    const msg = input.value.trim();
    if (!msg) return;

    addUserMessage(msg);
    input.value = "";

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        let botReply = "";
        if (data && data.reply) botReply = data.reply;
        else botReply = "⚠️ Server did not send a reply";

        addBotMessage(botReply);

    } catch (err) {
        addBotMessage("❌ Cannot connect to server");
    }
}





