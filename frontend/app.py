import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Tutor — RAG-Based Learning Assistant")

# 2. CRITICAL INITIALIZATION: Set up session_id right here!
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 3. Initialize your messages list as well to prevent the next crash
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── SIDEBAR: PDF Upload ──────────────────────
with st.sidebar:
    st.header("📄 Upload Course Material")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    st.caption(f"Session: {st.session_state.session_id[:8]}...")
    
    # Clear memory button
    if st.button("🔄 Clear Chat History"):
        requests.post(
            f"{API_URL}/clear-memory",
            json={"session_id": st.session_state.session_id}
        )
        st.session_state.messages = []
        st.rerun()

    if uploaded_file and st.button("Ingest PDF"):
        with st.spinner("Processing PDF..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }
            response = requests.post(
                f"{API_URL}/ingest",
                files=files
            )
            if response.status_code == 200:
                data = response.json()
                st.success(
                    f"✅ Ingested {data['chunks_created']} chunks!"
                )
            else:
                st.error(f"❌ Error: {response.text}")

# ── MAIN: Chat ───────────────────────────────
st.header("💬 Ask a Question")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources"):
                for src in msg["sources"]:
                    st.write(
                        f"Page {src['page']}: {src['snippet']}"
                    )

# Chat input
user_question = st.text_input("Type your question here...")

if st.button("Ask") and user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": user_question,
                    "session_id": "default"
                }
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", [])
                })
                st.rerun()
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")