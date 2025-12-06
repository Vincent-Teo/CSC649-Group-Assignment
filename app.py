import streamlit as st
from openai import OpenAI

# Load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --------- Page Config ---------
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="wide")

# --------- Custom CSS for Chat Bubbles + Input at Bottom ---------
bubble_style = """
<style>
/* Chat bubble container */
.chat-bubble {
    padding: 12px 18px;
    margin: 10px 0;
    border-radius: 18px;
    max-width: 80%;
    display: inline-block;
    line-height: 1.5;
    font-size: 18px;
}

/* User bubble (right side) */
.user-bubble {
    background-color: #4F8BF9;
    color: white;
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 5px;
}

/* Bot bubble (left side) */
.bot-bubble {
    background-color: #303030;
    color: #f5f5f5;
    margin-right: auto;
    border-bottom-left-radius: 5px;
}

/* Fix input box to bottom */
.stChatInputContainer {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background: rgba(20,20,20,0.95);
    backdrop-filter: blur(5px);
    z-index: 999;
    border-top: 1px solid #444;
}
</style>
"""
st.markdown(bubble_style, unsafe_allow_html=True)

# --------- Crisis Keywords ---------
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "i want to die", "hurt myself", "cut myself"
]

def is_crisis_message(msg):
    text = msg.lower()
    return any(keyword in text for keyword in CRISIS_KEYWORDS)

# --------- Session State for Chat ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------- Title ---------
st.markdown("<h1 style='text-align:center;'>🧠 Mental Health Support Chatbot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color: #ccc;'>This chatbot provides emotional support, "
    "but it is not a replacement for professional help.</p>",
    unsafe_allow_html=True
)
st.write("")

# --------- Display Chat History ---------
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div class='chat-bubble user-bubble'>🧑‍💬 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot-bubble'>🤖 {msg}</div>", unsafe_allow_html=True)

# --------- Input Box (fixed at bottom) ---------
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Save user message
    st.session_state.chat_history.append(("user", user_input))

    # Crisis detection
    if is_crisis_message(user_input):
        crisis_reply = (
            "I'm really sorry you're feeling this way. "
            "Your feelings matter and you deserve support.\n\n"
            "**Emergency Resources:**\n"
            "📞 Contact your local emergency number\n"
            "💬 Talk to a trusted friend or family member\n"
            "☎️ Call a mental health hotline\n\n"
            "You’re not alone — please seek help immediately."
        )
        st.session_state.chat_history.append(("bot", crisis_reply))
        st.rerun()

    # OpenAI response
    system_prompt = """
    You are a mental health support chatbot.
    Provide empathetic, calming, supportive responses.
    Do NOT give medical advice or diagnoses.
    Speak gently, warmly, and reassuringly.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
    )

    bot_reply = response.choices[0].message.content
    st.session_state.chat_history.append(("bot", bot_reply))

    st.rerun()
