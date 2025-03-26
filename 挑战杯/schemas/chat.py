from pydantic import BaseModel

class ChatMessage(BaseModel):
    question: str
    answer: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]