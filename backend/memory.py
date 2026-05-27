from langchain.memory import ConversationBufferMemory

# Store one memory object per session
_sessions: dict = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    """Return existing memory or create new one."""
    if session_id not in _sessions:
        _sessions[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    return _sessions[session_id]

def clear_memory(session_id: str):
    """Reset conversation history for a session."""
    if session_id in _sessions:
        del _sessions[session_id]

def get_all_sessions() -> list:
    """Return list of all active session IDs."""
    return list(_sessions.keys())