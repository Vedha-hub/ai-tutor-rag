import streamlit as st
import requests

# ── Config ─────────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Tutor", page_icon="🎓", layout="wide")

# ── Session State Init ────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(__import__("uuid").uuid4())[:8]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"question": ..., "answer": ..., "sources": [...]}

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Course Material")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        st.write(f"**{uploaded_file.name}**")
        st.write(f"{uploaded_file.size / 1024:.1f} KB")

        if st.button("📥 Ingest PDF", use_container_width=True):
            with st.spinner("Processing PDF... this may take a minute"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/ingest", files=files, timeout=300)

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ Ingested {data.get('chunks_created', '?')} chunks from {uploaded_file.name}")
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    st.divider()

    # ── Ingested Documents List ───────────────────────────────────────────────
    st.subheader("📚 Ingested Documents")
    try:
        response = requests.get(f"{API_URL}/documents", timeout=10)
        if response.status_code == 200:
            docs = response.json().get("documents", [])
            if docs:
                for doc in docs:
                    st.write(f"• {doc['filename']} ({doc['chunks_created']} chunks)")
            else:
                st.caption("No documents ingested yet")
    except Exception:
        st.caption("Backend not reachable")

    st.divider()
    st.caption(f"Session: {st.session_state.session_id}")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
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


# ── Main Page ─────────────────────────────────────────────────────────────────
st.title("🎓 AI Tutor — RAG-Based Learning Assistant")

# ── Ask a Question Section ──────────────────────────────────────────────────
st.header("💬 Ask a Question")

# Display chat history
for turn in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.write(turn["answer"])
        if turn.get("sources"):
            with st.expander("📖 Sources"):
                for s in turn["sources"]:
                    st.markdown(
                        f"**{s.get('source', 'unknown')}** — Page {s.get('page', '?')} "
                        f"(score: {s.get('score', 'N/A')})"
                    )
                    st.caption(s.get("snippet", ""))

# Question input
question = st.chat_input("Type your question here...")

if question:
    # Show user message immediately
    with st.chat_message("user"):
        st.write(question)

    # Get answer with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question, "session_id": st.session_state.session_id},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])

                    st.write(answer)

                    if sources:
                        with st.expander("📖 Sources"):
                            for s in sources:
                                st.markdown(
                                    f"**{s.get('source', 'unknown')}** — Page {s.get('page', '?')} "
                                    f"(score: {s.get('score', 'N/A')})"
                                )
                                st.caption(s.get("snippet", ""))

                    # Save to session history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })

                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"❌ {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


st.divider()

# ── Generate Quiz Section ────────────────────────────────────────────────────
st.header("📝 Generate Quiz")

topic = st.text_input("Enter topic for quiz:", placeholder="e.g. image processing, histogram")

col1, col2 = st.columns([1, 4])
with col1:
    generate_clicked = st.button("🎯 Generate Quiz", use_container_width=True)

if generate_clicked:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating quiz questions..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate-quiz",
                    json={"topic": topic},
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()
                    questions = data.get("questions", [])

                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.success(f"✅ Generated {len(questions)} questions on '{topic}'")
                    else:
                        st.warning("⚠️ No quiz could be generated. Try a different topic or make sure relevant content is ingested.")
                        st.session_state.quiz_questions = []
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"❌ {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ── Display Quiz ──────────────────────────────────────────────────────────────
if st.session_state.quiz_questions:
    st.subheader("Quiz")

    for i, q in enumerate(st.session_state.quiz_questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        selected = st.radio(
            label="",
            options=q["options"],
            key=f"quiz_q_{i}",
            index=None,
            disabled=st.session_state.quiz_submitted
        )
        st.session_state.quiz_answers[i] = selected
        st.write("")  # spacing

    if not st.session_state.quiz_submitted:
        if st.button("✅ Submit Quiz"):
            st.session_state.quiz_submitted = True
            st.rerun()

    # ── Show Results ────────────────────────────────────────────────────────
    if st.session_state.quiz_submitted:
        score = 0
        total = len(st.session_state.quiz_questions)

        for i, q in enumerate(st.session_state.quiz_questions):
            selected = st.session_state.quiz_answers.get(i)
            correct_letter = q.get("answer", "").strip().upper()

            is_correct = (
                selected is not None
                and selected.strip().upper().startswith(correct_letter)
            )

            if is_correct:
                score += 1

            with st.container():
                if is_correct:
                    st.success(f"Q{i+1}: Correct! ✅")
                else:
                    st.error(f"Q{i+1}: Incorrect ❌")
                    st.write(f"Your answer: {selected if selected else 'No answer selected'}")

                # Find and show the correct option text
                correct_option = next(
                    (opt for opt in q["options"] if opt.strip().upper().startswith(correct_letter)),
                    correct_letter
                )
                st.write(f"**Correct answer:** {correct_option}")
                if q.get("explanation"):
                    st.caption(f"💡 {q['explanation']}")

        st.divider()
        percentage = (score / total) * 100 if total > 0 else 0
        st.metric("Your Score", f"{score} / {total}", f"{percentage:.0f}%")

        if st.button("🔄 Try Another Quiz"):
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()