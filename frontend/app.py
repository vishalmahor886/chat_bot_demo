import streamlit as st
import requests
import uuid
import os

API_URL = "http://127.0.0.1:8000/chat"
UPLOAD_URL = "http://127.0.0.1:8000/upload-pdf"
LIST_PDFS_URL = "http://127.0.0.1:8000/list-pdfs"
DELETE_PDF_URL = "http://127.0.0.1:8000/delete-pdf"

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="AI Chatbot with PDF",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------
# HELPER FUNCTIONS
# --------------------------------
def fetch_pdfs(thread_id):
    try:
        response = requests.get(LIST_PDFS_URL, params={"thread_id": thread_id})
        if response.status_code == 200:
            return response.json().get("pdfs", [])
    except:
        pass
    return []

def delete_pdf(filename, thread_id):
    try:
        requests.delete(f"{DELETE_PDF_URL}/{filename}", params={"thread_id": thread_id})
    except:
        pass

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
    
    # Render chat buttons
    for tid, title in st.session_state.chats.items():
        if st.button(title, key=f"chat_{tid}", use_container_width=True):
            st.session_state.thread_id = tid
            st.rerun()
            
    st.markdown("---")
    st.subheader("📄 Upload PDF")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf"], key=f"uploader_{st.session_state.thread_id}")
    if uploaded_file:
        if st.button("Upload to Chat", use_container_width=True):
            with st.spinner("Uploading & processing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(UPLOAD_URL, files=files, params={"thread_id": st.session_state.thread_id})
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Uploaded {uploaded_file.name} ({data.get('pages', '?')} pages)")
                    else:
                        st.error(f"Failed to upload: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
            
    st.subheader("📚 Attached PDFs")
    pdfs = fetch_pdfs(st.session_state.thread_id)
    if pdfs:
        for pdf in pdfs:
            col1, col2 = st.columns([0.8, 0.2])
            col1.write(f"📄 {pdf}")
            if col2.button("❌", key=f"del_{pdf}"):
                delete_pdf(pdf, st.session_state.thread_id)
                st.rerun()
    else:
        st.info("No PDFs attached to this chat yet.")

# --------------------------------
# CURRENT CHAT
# --------------------------------
current_thread = st.session_state.thread_id
chat_history = st.session_state.chat_data[current_thread]

st.title("🤖 AI Chatbot")

pdfs_in_chat = fetch_pdfs(current_thread)
if pdfs_in_chat:
    st.caption(f"🧠 Context active: {len(pdfs_in_chat)} PDF(s) loaded")
else:
    st.caption("🌐 Web search only")

# --------------------------------
# DISPLAY MESSAGES
# --------------------------------
for sender, message in chat_history:
    role = "user" if sender == "You" else "assistant"
    with st.chat_message(role):
        st.markdown(message)

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
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
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
                    text = chunk.decode("utf-8", errors="ignore")
                    bot_reply += text
                    placeholder.markdown(bot_reply + "▌")

            placeholder.markdown(bot_reply)

        except Exception as e:
            bot_reply = f"Backend Error: {str(e)}"
            placeholder.markdown(bot_reply)

    # Save bot response
    chat_history.append(("Bot", bot_reply))
    st.session_state.chat_data[current_thread] = chat_history
