// memory บนหน้าเว็บ
let chatHistory = [];

// แสดงข้อความในกล่องแชท
function showMessage(text, sender) {
    let box = document.getElementById("chat-box");
    let div = document.createElement("div");

    div.className = sender === "user" ? "user-msg" : "ai-msg";
    div.innerText = text;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

// ส่งข้อความไป backend
async function sendMessage() {
    let input = document.getElementById("message");
    let msg = input.value.trim();
    if (!msg) return;

    // ล้างช่องข้อความ
    input.value = "";

    // แสดงที่หน้าจอ
    showMessage(msg, "user");

    // เก็บ history
    chatHistory.push({
        role: "user",
        content: msg
    });

    // ส่งไป Flask
    let res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });

    let data = await res.json();
    showMessage(data.reply, "ai");
}
