import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main { background-color: #0e1117; }
.title-text {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.subtitle-text {
    text-align: center;
    color: #888;
    margin-bottom: 1.5rem;
}
section[data-testid="stSidebar"] { background-color: #131720; }
</style>
""", unsafe_allow_html=True)

# ---------- Session state init ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None


def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"title": "New Chat", "messages": []}
    st.session_state.active_chat = chat_id


if not st.session_state.chats:
    new_chat()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 💬 Chats")
    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown("---")

    for chat_id in reversed(list(st.session_state.chats.keys())):
        title = st.session_state.chats[chat_id]["title"]
        is_active = chat_id == st.session_state.active_chat
        label = f"🟢 {title}" if is_active else title
        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.active_chat = chat_id
            st.rerun()

# ---------- Main area ----------
st.markdown('<p class="title-text">🤖 Simple Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Powered by Amazon Nova Pro via Bedrock</p>', unsafe_allow_html=True)

active_id = st.session_state.active_chat
active_chat = st.session_state.chats[active_id]

# ---------- Show past messages ----------
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Fixed chat input at bottom ----------
user_input = st.chat_input("Search the topic you want...")

if user_input:
    # show user message immediately
    active_chat["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # set title from first question
    if active_chat["title"] == "New Chat":
        active_chat["title"] = user_input[:30] + ("..." if len(user_input) > 30 else "")

    # get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"question": user_input}
                )
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    active_chat["messages"].append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ FastAPI server not running. Start it with `uvicorn main:app --reload --port 8000`")