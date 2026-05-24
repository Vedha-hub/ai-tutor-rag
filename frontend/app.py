# frontend/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Tutor", page_icon="🎓", layout="wide")
st.title("🎓 AI Tutor — RAG-Based Learning Assistant")

# ── SIDEBAR: PDF Upload ──────────────────────────────
with st.sidebar:
    st.header("📄 Upload Course Material")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file and st.button("Ingest PDF"):
        with st.spinner("Processing PDF..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/ingest", files=files)
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Ingested {data['chunks_created']} chunks!")
            else:
                st.error(f"❌ Error: {response.text}")

# ── MAIN: Chat Area (wired to /ask in Week 2) ────────
st.header("💬 Ask a Question")
user_question = st.text_input("Type your question here...")

if st.button("Ask") and user_question:
    st.info("Chat endpoint coming in Week 2!")