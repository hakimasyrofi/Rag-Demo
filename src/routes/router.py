from fastapi import APIRouter
from ..models.schemas import QuestionRequest, QuestionResponse, DocumentRequest, DocumentResponse
from ..controllers.rag_controller import RagController

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
def ask_question(req: QuestionRequest):
    return RagController.ask_question(req)

@router.post("/add", response_model=DocumentResponse)
def add_document(req: DocumentRequest):
    return RagController.add_document(req)

@router.get("/status")
def status():
    return RagController.get_status()
