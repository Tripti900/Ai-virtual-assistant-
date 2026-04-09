from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# ✅ Load environment variables (.env file)
load_dotenv()

app = Flask(__name__)

# ✅ Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Home route
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Chat/Ask route (frontend will call this)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        mode = data.get("mode", "teaching")  # 🟣 Get mode from frontend (default = teaching)

        if not user_input:
            return jsonify({"reply": "⚠️ Please say or type something!"})

        # 🧠 Define behavior based on mode
        if mode == "coding":
            system_prompt = "You are an expert AI Coding Assistant. Help students write and debug code with examples."
        elif mode == "doubt":
            system_prompt = "You are a friendly AI Doubt Solver. Give clear and short answers to student questions."
        else:
            system_prompt = "You are an AI Teaching Assistant helping students understand topics in simple words."

        # 🧠 Generate AI reply using Groq model
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Working Groq model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        reply = chat_completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Server Error:", e)
        return jsonify({"reply": f"⚠️ Server error: {str(e)}"})

# ✅ Run Flask app
if __name__ == "__main__":
    app.run(debug=True)