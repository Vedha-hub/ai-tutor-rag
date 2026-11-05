import streamlit as st
import requests
import uuid

# ── Config ─────────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
}

/* Hero title */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    line-height: 1.2;
}

.hero-sub {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 32px;
}

/* Section headers */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Doc badge */
.doc-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #c4b5fd;
    margin: 3px;
}

/* Chat messages */
.chat-user {
    background: linear-gradient(135deg, rgba(167,139,250,0.2), rgba(96,165,250,0.2));
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    color: #e2e8f0;
    margin-bottom: 8px;
    margin-left: 20%;
}

.chat-bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    color: #cbd5e1;
    margin-bottom: 8px;
    margin-right: 10%;
}

/* Score badge */
.score-badge {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #34d399, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    padding: 8px 20px !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stChatInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(167,139,250,0.4) !important;
    border-radius: 12px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}

/* Radio buttons */
.stRadio > div {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 8px;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Success / Error */
.stSuccess {
    background: rgba(52,211,153,0.1) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    border-radius: 10px !important;
}
.stError {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: 10px !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "ingested_docs" not in st.session_state:
    st.session_state.ingested_docs = []


# ── Helper: fetch docs ─────────────────────────────────────────────────────────
def fetch_docs():
    try:
        r = requests.get(f"{API_URL}/documents", timeout=10)
        if r.status_code == 200:
            st.session_state.ingested_docs = r.json().get("documents", [])
    except Exception:
        pass


# Fetch docs on load
fetch_docs()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 AI Tutor")
    st.markdown("---")

    st.markdown("**📄 Upload Course Material**")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        st.markdown(f"**{uploaded_file.name}** · {uploaded_file.size/1024:.1f} KB")

        if st.button("📥 Ingest PDF", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    resp = requests.post(f"{API_URL}/ingest", files=files, timeout=300)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.success(f"✅ {data.get('chunks_created','?')} chunks ingested!")
                        fetch_docs()
                        st.rerun()
                    else:
                        st.error(f"❌ {resp.json().get('detail','Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not running on port 8000")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    st.markdown("---")

    # Ingested docs
    st.markdown("**📚 Ingested Documents**")
    if st.session_state.ingested_docs:
        for doc in st.session_state.ingested_docs:
            st.markdown(
                f'<span class="doc-badge">📄 {doc["filename"]} · {doc["chunks_created"]} chunks</span>',
                unsafe_allow_html=True
            )
        if st.button("🗑️ Clear Document History", use_container_width=True):
            for doc in st.session_state.ingested_docs:
                try:
                    requests.delete(
                        f"{API_URL}/documents",
                        json={"filename": doc["filename"]},
                        timeout=30
                    )
                except Exception:
                    pass
            st.session_state.ingested_docs = []
            st.success("Document history cleared!")
            st.rerun()
    else:
        st.caption("No documents ingested yet")

    st.markdown("---")
    st.caption(f"Session: `{st.session_state.session_id}`")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 Clear Chat", use_container_width=True):
            try:
                requests.post(
                    f"{API_URL}/clear-memory",
                    json={"session_id": st.session_state.session_id},
                    timeout=10
                )
            except Exception:
                pass
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        if st.button("📝 Clear Quiz", use_container_width=True):
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()


# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎓 AI Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">RAG-Based Learning Assistant — Ask questions from your course materials</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Ask a Question", "📝 Generate Quiz"])

# ── TAB 1: Chat ────────────────────────────────────────────────────────────────
with tab1:
    # Chat history display
    if st.session_state.chat_history:
        for turn in st.session_state.chat_history:
            st.markdown(f'<div class="chat-user">🧑 {turn["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bot">🤖 {turn["answer"]}</div>', unsafe_allow_html=True)
            if turn.get("sources"):
                with st.expander("📖 View Sources"):
                    for s in turn["sources"]:
                        st.markdown(f"**{s.get('source','unknown')}** — Page {s.get('page','?')} · Score: {s.get('score','N/A')}")
                        st.caption(s.get("snippet",""))
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:40px;">
            <div style="font-size:2.5rem; margin-bottom:12px;">💬</div>
            <div style="color:#94a3b8; font-size:1rem;">Upload a PDF and start asking questions about your course material</div>
        </div>
        """, unsafe_allow_html=True)

    # Chat input
    question = st.chat_input("Ask anything about your course material...")
    if question:
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question, "session_id": st.session_state.session_id},
                    timeout=180
                )
                if resp.status_code == 200:
                    result = resp.json()
                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })
                    st.rerun()
                else:
                    st.error(f"❌ {resp.json().get('detail','Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running on port 8000")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out — Gemini is slow on free tier, please try again")
            except Exception as e:
                st.error(f"❌ {str(e)}")


# ── TAB 2: Quiz ────────────────────────────────────────────────────────────────
with tab2:
    if not st.session_state.quiz_questions:
        st.markdown('<div class="section-title">Generate a Quiz</div>', unsafe_allow_html=True)

        topic = st.text_input("Enter topic:", placeholder="e.g. linear regression, neural networks")

        if st.button("🎯 Generate Quiz", use_container_width=False):
            if not topic.strip():
                st.warning("Please enter a topic first.")
            else:
                with st.spinner("Generating 5 questions..."):
                    try:
                        resp = requests.post(
                            f"{API_URL}/generate-quiz",
                            json={"topic": topic},
                            timeout=180
                        )
                        if resp.status_code == 200:
                            questions = resp.json().get("questions", [])
                            if questions:
                                st.session_state.quiz_questions = questions
                                st.session_state.quiz_answers = {}
                                st.session_state.quiz_submitted = False
                                st.rerun()
                            else:
                                st.warning("⚠️ No questions generated — try a more specific topic or ingest more content.")
                        else:
                            st.error(f"❌ {resp.json().get('detail','Unknown error')}")
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out — please try again")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")

    else:
        # Show quiz
        if not st.session_state.quiz_submitted:
            st.markdown(f'<div class="section-title">📝 Answer all 5 questions</div>', unsafe_allow_html=True)

            for i, q in enumerate(st.session_state.quiz_questions):
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="color:#a78bfa; font-size:0.8rem; font-weight:600; margin-bottom:6px;">QUESTION {i+1} OF {len(st.session_state.quiz_questions)}</div>
                        <div style="color:#e2e8f0; font-size:1rem; font-weight:500;">{q['question']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    selected = st.radio(
                    label=f"Question {i+1}",
                    options=q["options"],
                    key=f"q_{i}",
                    index=None,
                    label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[i] = selected

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✅ Submit Quiz", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            with col2:
                if st.button("🔄 New Quiz", use_container_width=True):
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()

        else:
            # Results
            score = 0
            total = len(st.session_state.quiz_questions)

            for i, q in enumerate(st.session_state.quiz_questions):
                selected = st.session_state.quiz_answers.get(i)
                correct_letter = q.get("answer", "").strip().upper()
                is_correct = selected is not None and selected.strip().upper().startswith(correct_letter)
                if is_correct:
                    score += 1

            percentage = (score / total) * 100 if total > 0 else 0

            # Score display
            st.markdown(f"""
            <div class="card" style="text-align:center; padding:32px;">
                <div style="color:#94a3b8; font-size:0.9rem; margin-bottom:8px;">YOUR SCORE</div>
                <div class="score-badge">{score}/{total}</div>
                <div style="color:#94a3b8; font-size:1.1rem; margin-top:8px;">{percentage:.0f}% — {"🎉 Excellent!" if percentage >= 80 else "👍 Good effort!" if percentage >= 50 else "📚 Keep studying!"}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # Per-question review
            for i, q in enumerate(st.session_state.quiz_questions):
                selected = st.session_state.quiz_answers.get(i)
                correct_letter = q.get("answer", "").strip().upper()
                is_correct = selected is not None and selected.strip().upper().startswith(correct_letter)

                correct_option = next(
                    (opt for opt in q["options"] if opt.strip().upper().startswith(correct_letter)),
                    correct_letter
                )

                color = "#34d399" if is_correct else "#f87171"
                icon = "✅" if is_correct else "❌"

                st.markdown(f"""
                <div class="card" style="border-left: 3px solid {color};">
                    <div style="color:{color}; font-size:0.8rem; font-weight:600; margin-bottom:6px;">{icon} Q{i+1} — {"Correct" if is_correct else "Incorrect"}</div>
                    <div style="color:#e2e8f0; margin-bottom:8px;">{q['question']}</div>
                    <div style="color:#94a3b8; font-size:0.85rem;">Your answer: {selected if selected else "Not answered"}</div>
                    <div style="color:{color}; font-size:0.85rem;">Correct answer: {correct_option}</div>
                    {"<div style='color:#64748b; font-size:0.82rem; margin-top:6px;'>💡 " + q.get('explanation','') + "</div>" if q.get('explanation') else ""}
                </div>
                """, unsafe_allow_html=True)

            if st.button("🔄 Try Another Quiz", use_container_width=False):
                st.session_state.quiz_questions = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()