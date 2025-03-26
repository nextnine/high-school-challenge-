from collections import defaultdict

class ContextManager:
    def __init__(self):
        self.sessions = defaultdict(list)
        self.max_history = 5

    def get_history(self, session_id: str):
        return self.sessions[session_id][-self.max_history:]
    
    def update_history(self, session_id: str, question: str, answer: str):
        self.sessions[session_id].append((question, answer))
    
    def clear_history(self, session_id: str):
        del self.sessions[session_id]

context_manager = ContextManager()