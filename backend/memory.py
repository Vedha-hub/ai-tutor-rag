from langchain.memory import ConversationBufferMemory

# Store one memory object per session
_sessions: dict = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    """Return existing memory or create new one."""
    if session_id not in _sessions:
        _sessions[session_id] = ConversationBufferMemory()
    return _sessions[session_id]

def add_to_memory(session_id: str, user_message: str, ai_message: str):
    memory = get_memory(session_id)
    memory.save_context({"input": user_message}, {"output": ai_message})

def get_chat_history(session_id: str):
    memory = get_memory(session_id)
    return memory.load_memory_variables({}).get("history", "")

def clear_memory(session_id: str):
    if session_id in _sessions:
        del _sessions[session_id]


def get_all_sessions() -> list:
    return list(_sessions.keys())