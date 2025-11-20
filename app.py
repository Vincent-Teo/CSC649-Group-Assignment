from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Crisis keywords for safety check
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "i want to die", "hurt myself", "cut myself"
]

def is_crisis_message(message):
    """Check if user message contains crisis-related words."""
    text = message.lower()
    return any(keyword in text for keyword in CRISIS_KEYWORDS)

# ---------- HOME ROUTE (Serves index.html) ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- CHAT ROUTE (Handles chatbot responses) ----------
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Crisis Handling
    if is_crisis_message(user_message):
        crisis_response = (
            "I'm really sorry that you're feeling this way. "
            "Your feelings matter, and you deserve support. "
            "I’m not able to help in emergencies, but please reach out to someone who can help immediately.\n\n"
            "📞 Emergency Resources:\n"
            "- Contact your local emergency number\n"
            "- Reach out to a trusted friend or family member\n"
            "- Call your nearest mental health crisis hotline\n\n"
            "You aren’t alone—please seek immediate help."
        )
        return jsonify({"response": crisis_response})

    # Safe system prompt
    system_prompt = """
    You are a mental health support chatbot.
    Provide empathetic, calming, and supportive responses.
    Do NOT give professional medical advice or diagnoses.
    Use simple, warm, comforting language.
    If user mentions suicide or self-harm, DO NOT answer normally. Trigger crisis safety message.
    """

    # OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    bot_reply = response.choices[0].message.content
    return jsonify({"response": bot_reply})


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
