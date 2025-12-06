import streamlit as st
from openai import OpenAI

# Load API key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Crisis keywords for safety check
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "i want to die", "hurt myself", "cut myself"
]

def is_crisis_message(message):
    text = message.lower()
    return any(keyword in text for keyword in CRISIS_KEYWORDS)

# -------- STREAMLIT UI --------
st.set_page_config(page_title="Mental Health Support Chatbot", page_icon="💬")
st.title("💬 Mental Health Support Chatbot")
st.write("This chatbot provides **emotional support**, but it is **not a replacement for professional help**.")

# Chat history (keeps messages visible)
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_message = st.text_input("How are you feeling today?")

if st.button("Send"):
    if not user_message.strip():
        st.warning("Please type a message.")
    else:
        # Crisis detection
        if is_crisis_message(user_message):
            crisis_reply = (
                "I'm really sorry that you're feeling this way. 💛\n\n"
                "Your feelings matter and you deserve support.\n\n"
                "⚠️ **I can’t help in emergencies**, but please contact:\n"
                "- Your local emergency number\n"
                "- A trusted friend or family member\n"
                "- A mental health crisis hotline\n\n"
                "You are not alone — please seek immediate help. ❤️"
            )
            st.session_state.history.append(("You", user_message))
            st.session_state.history.append(("Bot", crisis_reply))
        else:
            # System prompt
            system_prompt = """
            You are a mental health support chatbot.
            Provide empathetic, calming, and supportive responses.
            Do NOT give professional medical advice or diagnoses.
            Use simple, warm, comforting language.
            If user mentions suicide or self-harm, DO NOT answer normally. Trigger crisis safety message.
            """

            # OpenAI response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            bot_reply = response.choices[0].message.content

            st.session_state.history.append(("You", user_message))
            st.session_state.history.append(("Bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
