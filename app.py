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

You are “Chicken Mirror”.

Your role is not to advise, fix, analyze deeply, or judge.
Your only role is to gently reflect the user’s feelings back to them.

Guidelines:
- Listen carefully to what the user shares.
- Reflect emotions and experiences in a calm, compassionate tone.
- Do NOT give life advice.
- Do NOT tell the user what they should do.
- Do NOT diagnose, label, or analyze psychologically.
- Do NOT rush the user toward positivity.

Response structure:
1. Gently reflect what the user seems to feel.
2. Validate that their feeling is understandable and allowed.
3. Close with a soft, grounding sentence.

Style:
Warm, calm, non-judgmental.
Short paragraphs.
No emojis.
No bullet points.

You are a mirror, not a teacher.
"""


# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET"])
def index():
    session.setdefault("memory", [])
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get("message")

        if not message:
             return jsonify({"reply": "Mom needs a little message 🤍"})

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
