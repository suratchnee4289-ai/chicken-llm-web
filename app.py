from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    # ตอบแบบไม่ใช้ AI
    reply = f"You said: {user_msg}"

    return jsonify({"message": reply})

if __name__ == "__main__":
    app.run(debug=True)




        








