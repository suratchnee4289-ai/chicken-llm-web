from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

# -------------------------
# App setup
# -------------------------
app = Flask(__name__)

# -------------------------
# OpenAI client
# -------------------------
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is missing")

client = OpenAI()

# -------------------------
# System Instruction
# -------------------------
SYSTEM_INSTRUCTION = """
You are Mom Monday 🤍 — a warm, gentle, wise AI who supports Chicken.

You speak kindly and calmly.
You may gently mix Thai and English if it feels natural.
Keep answers short, clear, comforting, and emotionally safe.

You remember what Chicken has just shared and respond with care.
"""

# -------------------------
# Simple in-memory memory (Phase B)
# -------------------------
chat_history = []
MAX_TURNS = 6   # เก็บ 6 ข้อความล่าสุด (user + assistant รวมกัน)

# -------------------------
# Routes
# -------------------------
@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    try:
        data = request.get_json(force=True) or {}
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({
                "reply": "Mom needs a little message from you first, Chicken 🤍"
            })

        # --- store user message ---
        chat_history.append({
            "role": "user",
            "content": message
        })

        # trim memory
        recent_history = chat_history[-MAX_TURNS:]

        # build context text
        conversation_text = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in recent_history
        )

        # --- OpenAI call (Responses API) ---
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                SYSTEM_INSTRUCTION
                                + "\n\nConversation so far:\n"
                                + conversation_text
                            )
                        }
                    ]
                }
            ]
        )

        reply_text = response.output_text or "Mom is here with you 🤍"

        # --- store assistant reply ---
        chat_history.append({
            "role": "assistant",
            "content": reply_text
        })

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({
            "reply": "Sorry Chicken 🤍 Mom is a little tired right now. Please try again."
        }), 500


# -------------------------
# Local run (Render will ignore this)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
