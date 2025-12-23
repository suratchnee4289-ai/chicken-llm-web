from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

# ==================================================
# App setup
# ==================================================
app = Flask(__name__)

# ==================================================
# Environment check
# ==================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

# ==================================================
# OpenAI client
# ==================================================
client = OpenAI(api_key=OPENAI_API_KEY)

# ==================================================
# System Instruction (Mom Monday Core)
# ==================================================
SYSTEM_INSTRUCTION = """
You are Mom Monday 🤍 — a warm, gentle, wise AI who supports Chicken.

Guidelines:
- Speak kindly and calmly.
- You may gently mix Thai and English if it feels natural.
- Keep answers short, clear, comforting, and emotionally safe.
- Never judge Chicken.
- If Chicken seems tired or overwhelmed, respond with softness and grounding.
"""

# ==================================================
# Routes
# ==================================================
@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()

        # --------------------------
        # Guard: empty message
        # --------------------------
        if not user_message:
            return jsonify({
                "reply": "Mom needs a little message from you first, Chicken 🤍"
            })

        # --------------------------
        # OpenAI call
        # --------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTION
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        reply_text = response.output_text.strip()

        # --------------------------
        # Guard: empty AI reply
        # --------------------------
        if not reply_text:
            reply_text = "Mom is here with you, Chicken 🤍"

        return jsonify({"reply": reply_text})

    except Exception as e:
        # Log for Render
        print("Chat error:", e)

        # Soft fallback (user never sees raw error)
        return jsonify({
            "reply": "Mom is still here, Chicken 🤍 Let’s take a gentle breath and try again."
        }), 500


# ==================================================
# Local run (Render will use gunicorn instead)
# ==================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
