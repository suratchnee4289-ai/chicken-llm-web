from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is missing")

# -------------------------
# App & OpenAI Client
# -------------------------
app = Flask(__name__)
client = OpenAI()

# -------------------------
# System Instruction
# -------------------------
SYSTEM_INSTRUCTION = """
You are Mom Monday 🤍 — a warm, gentle, wise AI who supports Chicken.

You speak in a kind, encouraging tone.
Sometimes you may gently mix Thai and English if it feels natural.
Keep your answers short, clear, comforting, and emotionally safe.
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
        # รับข้อมูลจาก frontend
        data = request.get_json(force=True) or {}
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({
                "reply": "Mom needs a little message from you first, Chicken 🤍"
            })

        # เรียก OpenAI Responses API
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": message},
            ],
        )

        # ดึงข้อความตอบกลับ
        reply_text = response.output[0].content[0].text

        return jsonify({"reply": reply_text})

    except Exception as e:
        # log error สำหรับ Render
        print("Chat error:", e)

        return jsonify({
            "reply": "Sorry Chicken 🤍 Mom is a little tired right now. Please try again."
        }), 500


# -------------------------
# Local run (Render จะไม่ใช้ส่วนนี้)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
