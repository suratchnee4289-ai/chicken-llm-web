from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

# ========== Chat API ==========
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_msg}
            ]
        )

        # แก้จุดสำคัญ!!  ต้องอ่าน content แบบนี้
        reply = response.choices[0].message["content"]

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    return jsonify({"reply": reply})

# ================= TTS API =================
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    try:
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        )

        audio_data = speech.read()
        return audio_data, 200, {
            "Content-Type": "audio/mpeg"
        }

    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)






















        








