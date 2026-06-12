import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# 🎨 Advanced CSS + Animations
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e1e2f, #2c2c54);
    color: white;
}

.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg, .bot-msg {
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
    max-width: 75%;
    animation: fadeIn 0.3s ease-in-out;
}

.user-msg {
    background: #4CAF50;
    margin-left: auto;
    color: white;
}

.bot-msg {
    background: #3a3a5a;
    margin-right: auto;
    color:white;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Typing cursor */
.cursor {
    display: inline-block;
    width: 6px;
    background-color: white;
    margin-left: 3px;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50%, 100% {opacity: 1;}
    25%, 75% {opacity: 0;}
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1a1a2e;
    color:white;
}
div.stButton > button {
    background-color: #ff4b4b !important;   /* red */
    color: white !important;
    border-radius: 8px;
    padding: 8px 16px;
    border: none;
    font-weight: 600;
}

/* Hover effect */
div.stButton > button:hover {
    background-color: #ff1f1f !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🧠 Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.write("Model: Groq LLaMA 3.1")
    st.write("Streaming: Enabled ⚡")

# 🧠 Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 AI Chatbot")

# 📜 Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f'<div class="user-msg">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 💬 Input (bottom style)
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    # Show user instantly
    st.markdown(f'<div class="user-msg">{user_input}</div>', unsafe_allow_html=True)

    # Streaming response
    response = requests.post(
        API_URL,
        json={"message": user_input},
        stream=True
    )

    bot_reply = ""
    placeholder = st.empty()

    for chunk in response.iter_content(chunk_size=15):
        if chunk:
            text = chunk.decode("utf-8", errors="ignore")
            bot_reply += text

            placeholder.markdown(
                f'<div class="bot-msg">{bot_reply}<span class="cursor"></span></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.01)  # smooth animation

    # Final render
    placeholder.markdown(
        f'<div class="bot-msg">{bot_reply}</div>',
        unsafe_allow_html=True
    )

    st.session_state.chat_history.append(("Bot", bot_reply))
