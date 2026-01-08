import time
from fastapi import HTTPException
from ..services.rag_service import RagService
from ..services.storage_service import StorageService
from ..services.embedding_service import EmbeddingService
from ..models.schemas import QuestionRequest, DocumentRequest

embedding_service = EmbeddingService()
storage_service = StorageService()
rag_service = RagService(embedding_service, storage_service)

class RagController:
    @staticmethod
    def ask_question(req: QuestionRequest):
        start = time.time()
        try:
            result = rag_service.ask(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def add_document(req: DocumentRequest):
        try:
            emb = embedding_service.fake_embed(req.text)
            doc_id = storage_service.add_document(req.text, emb)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_status():
        base_status = storage_service.get_status()
        base_status["graph_ready"] = rag_service.workflow is not None
        return base_status
