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
"""

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

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": SYSTEM_INSTRUCTION + "\n\nUser: " + message
                        }
                    ]
                }
            ]
        )

        reply_text = response.output_text

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({
            "reply": "Sorry Chicken 🤍 Mom is a little tired right now. Please try again."
        }), 500


# -------------------------
# Local run only
# (Render จะไม่ใช้ส่วนนี้)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
