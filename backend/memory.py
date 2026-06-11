import time

_sessions: dict = {}

def get_memory(session_id: str) -> list:
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]

def add_to_memory(session_id: str, question: str, answer: str):
    memory = get_memory(session_id)
    memory.append({
        "question": question,
        "answer": answer,
        "timestamp": time.strftime("%H:%M:%S")
    })

def get_chat_history(session_id: str) -> str:
    memory = get_memory(session_id)
    if not memory:
        return ""
    history = ""
    for turn in memory[-5:]:
        history += f"Human: {turn['question']}\nAssistant: {turn['answer']}\n\n"
    return history.strip()

def clear_memory(session_id: str):
    if session_id in _sessions:
        del _sessions[session_id]

def get_all_sessions() -> list:
    return list(_sessions.keys())