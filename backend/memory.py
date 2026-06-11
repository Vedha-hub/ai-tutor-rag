# Simple in-memory session store — no langchain dependency needed

# Store one conversation history per session
_sessions: dict = {}


def get_memory(session_id: str) -> list:
    """Return existing conversation history or create new one."""
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]


def add_to_memory(session_id: str, question: str, answer: str):
    """Add a question/answer pair to session history."""
    memory = get_memory(session_id)
    memory.append({
        "question": question,
        "answer": answer
    })


def get_chat_history(session_id: str) -> str:
    """Return formatted chat history as a string for context."""
    memory = get_memory(session_id)
    if not memory:
        return ""
    history = ""
    for turn in memory[-5:]:  # only last 5 turns to avoid token overflow
        history += f"Human: {turn['question']}\nAssistant: {turn['answer']}\n\n"
    return history.strip()


def clear_memory(session_id: str):
    """Reset conversation history for a session."""
    if session_id in _sessions:
        del _sessions[session_id]


def get_all_sessions() -> list:
    """Return list of all active session IDs."""
    return list(_sessions.keys())