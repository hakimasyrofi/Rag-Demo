from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str] = []
    latency_sec: float

class DocumentRequest(BaseModel):
    text: str

class DocumentResponse(BaseModel):
    id: int
    status: str
