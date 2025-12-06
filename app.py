import streamlit as st
from openai import OpenAI
import time

# Page setup
st.set_page_config(page_title="Mental Health Chatbot", page_icon="💬", layout="wide")

# Load API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- CSS: LIGHT THEME + CHAT BUBBLES + FIXED INPUT ----------------
css = """
<style>
body {
    background-color: #f4f8ff !important;
}

/* Chat container spacing */
.chat-container {
    width: 100%;
    display: flex;
    margin: 10px 0;
}

/* User message bubble */
.user-msg {
    background: #99c9ff;
    color: #003366;
    padding: 12px 18px;
    border-radius: 16px;
    border-bottom-right-radius: 4px;
    margin-left: auto;
    max-width: 75%;
    font-size: 17px;
}

/* Bot message bubble */
.bot-msg {
    background: #e7f0ff;
    color: #003366;
    padding: 12px 18px;
    border-radius: 16px;
    border-bottom-left-radius: 4px;
    margin-right: auto;
    max-width: 75%;
    font-size: 17px;
}

/* Typing animation text */
.typing {
    color: #4a6fa5;
    font-style: italic;
    opacity: 0.8;
}

/* Fix input box at bottom */
.stChatInputContainer {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background: rgba(255,255,255,0.95);
    border-top: 1px solid #d0d0d0;
    backdrop-filter: blur(4px);
    z-index: 999;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------------- Crisis Keywords ----------------
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "i want to die", "hurt myself", "cut myself"
]

def is_crisis(text):
    text = text.lower()
    return any(k in text for k in CRISIS_KEYWORDS)

# ---------------- Session State ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Bot introduction message
    welcome = (
        "Hi there, I’m here to support you. 💙 "
        "You can talk to me about how you’re feeling. "
        "How are you today?"
    )
    st.session_state.chat_history.append(("bot", welcome))

if "typing" not in st.session_state:
    st.session_state.typing = False

# ---------------- Title ----------------
st.markdown("<h1 style='text-align:center; color:#003366;'>💬 Mental Health Support Chatbot</h1>", unsafe_allow_html=True)
st.write("")

# ---------------- Display Chat History ----------------
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div class='chat-container'><div class='user-msg'>🧑 {message}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='bot-msg'>🤖 {message}</div></div>", unsafe_allow_html=True)

# ---------------- Typing Indicator ----------------
if st.session_state.typing:
    st.markdown("<p class='typing'>🤖 Bot is typing…</p>", unsafe_allow_html=True)

# ---------------- Bottom Input ----------------
user_input = st.chat_input("Type your message…")

if user_input:
    # Add user's message
    st.session_state.chat_history.append(("user", user_input))

    # Crisis check
    if is_crisis(user_input):
        crisis_reply = (
            "I'm really sorry you're feeling this way. 💙\n\n"
            "**If you may be in danger, please reach out immediately:**\n"
            "📞 Call emergency services\n"
            "💬 Talk to someone you trust\n"
            "☎️ Contact a mental health hotline\n\n"
            "You’re not alone — please seek help right now."
        )
        st.session_state.chat_history.append(("bot", crisis_reply))
        st.rerun()

    # Show typing animation
    st.session_state.typing = True
    st.rerun()

if st.session_state.typing:
    # --------- Generate bot response ----------
    system_prompt = (
        "You are a gentle, empathetic emotional support chatbot. "
        "Write short, warm, comforting responses. No medical advice."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": st.session_state.chat_history[-1][1]}
        ]
    )

    bot_reply = response.choices[0].message.content

    # Simulate typing delay (feels more human)
    time.sleep(0.7)

    st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.typing = False
    st.rerun()
