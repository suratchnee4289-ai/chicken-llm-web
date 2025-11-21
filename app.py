from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__, template_folder="templates")

# 🔑 API KEY
api_key = os.getenv("")
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Chicken's assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        # ⭐ ใช้รูปแบบ API ใหม่
        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)



        







