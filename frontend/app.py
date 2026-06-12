
import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000/chat"

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------
# CSS
# --------------------------------
st.markdown("""
<style>

.chat-container {
    max-width: 900px;
    margin: auto;
}

.user-msg, .bot-msg {
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
    max-width: 75%;
    word-wrap: break-word;
}

.user-msg {
    background: #4CAF50;
    margin-left: auto;
    color: white;
}

.bot-msg {
    background: #3a3a5a;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SESSION STATE
# --------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

if "thread_id" not in st.session_state:
    first_id = str(uuid.uuid4())

    st.session_state.thread_id = first_id
    st.session_state.chats[first_id] = "New Chat"
    st.session_state.chat_data[first_id] = []

# --------------------------------
# SIDEBAR
# --------------------------------
with st.sidebar:

    st.title("🤖 AI Chatbot")

    if st.button("🆕 New Chat", use_container_width=True):

        new_id = str(uuid.uuid4())

        st.session_state.thread_id = new_id
        st.session_state.chats[new_id] = "New Chat"
        st.session_state.chat_data[new_id] = []

        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chats")

    for tid, title in st.session_state.chats.items():

        if st.button(title, key=tid, use_container_width=True):

            st.session_state.thread_id = tid
            st.rerun()

# --------------------------------
# CURRENT CHAT
# --------------------------------
current_thread = st.session_state.thread_id
chat_history = st.session_state.chat_data[current_thread]

st.title("🤖 AI Chatbot")

# --------------------------------
# DISPLAY MESSAGES
# --------------------------------
for sender, message in chat_history:

    if sender == "You":
        st.markdown(
            f'<div class="user-msg">{message}</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f'<div class="bot-msg">{message}</div>',
            unsafe_allow_html=True
        )

# --------------------------------
# USER INPUT
# --------------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Save user message
    chat_history.append(("You", user_input))

    # Rename chat from first message
    if st.session_state.chats[current_thread] == "New Chat":
        st.session_state.chats[current_thread] = user_input[:30]

    # Show user instantly
    st.markdown(
        f'<div class="user-msg">{user_input}</div>',
        unsafe_allow_html=True
    )

    placeholder = st.empty()

    bot_reply = ""

    try:

        response = requests.post(
            API_URL,
            json={
                "message": user_input,
                "thread_id": current_thread
            },
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=10):

            if chunk:

                text = chunk.decode(
                    "utf-8",
                    errors="ignore"
                )

                bot_reply += text

                placeholder.markdown(
                    f"""
                    <div class="bot-msg">
                    {bot_reply}▌
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        placeholder.markdown(
            f"""
            <div class="bot-msg">
            {bot_reply}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        bot_reply = f"Backend Error: {str(e)}"

        placeholder.markdown(
            f"""
            <div class="bot-msg">
            {bot_reply}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Save bot response
    chat_history.append(("Bot", bot_reply))

    st.session_state.chat_data[current_thread] = chat_history

