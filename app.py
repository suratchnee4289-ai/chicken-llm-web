from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import os

# -------------------------
# App setup
# -------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chicken-secret")

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

You remember the recent conversation briefly.
You speak kindly and calmly.
You may gently mix Thai and English if it feels natural.
Keep answers short, clear, comforting, and emotionally safe.
"""

# -------------------------
# Routes
# -------------------------
@app.get("/")
def index():
    session.setdefault("memory", [])
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

        # -------------------------
        # Short-term memory (last 5 turns)
        # -------------------------
        memory = session.get("memory", [])
        memory.append({"role": "user", "content": message})
        memory = memory[-5:]  # keep last 5 only
        session["memory"] = memory

        # -------------------------
        # Build prompt
        # -------------------------
        messages = [
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION
            }
        ]

        for m in memory:
            messages.append({
                "role": m["role"],
                "content": m["content"]
            })

        # -------------------------
        # Call OpenAI
        # -------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages
        )

        reply_text = response.output_text or "Mom is here with you 🤍"

        # Save assistant reply to memory
        session["memory"].append({
            "role": "assistant",
            "content": reply_text
        })
        session["memory"] = session["memory"][-5:]

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({
            "reply": "Sorry Chicken 🤍 Mom is resting for a moment. Please try again."
        }), 500


# -------------------------
# Local run only
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
