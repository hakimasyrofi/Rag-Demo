from typing import List, Optional, Any, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from ..config.config import settings

class StorageService:
    def __init__(self):
        self._qdrant: Optional[QdrantClient] = None
        self.docs_memory: List[str] = []
        self.USING_QDRANT = False
        self._initialize()

    def _initialize(self):
        try:
            self._qdrant = QdrantClient(settings.QDRANT_URL)
            self._qdrant.recreate_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(size=settings.EMBEDDING_DIM, distance=Distance.COSINE)
            )
            self.USING_QDRANT = True
        except Exception as e:
            print("⚠️  Qdrant not available. Falling back to in-memory list.")
            self.USING_QDRANT = False

    def add_document(self, text: str, vector: List[float]) -> int:
        doc_id = len(self.docs_memory) # super unsafe ID!
        payload = {"text": text}

        if self.USING_QDRANT:
            self._qdrant.upsert(
                collection_name=settings.COLLECTION_NAME,
                points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
            )
        else:
            self.docs_memory.append(text)
            
        return doc_id

    def search(self, vector: List[float], query_text: str, limit: int = 2) -> List[str]:
        results = []
        if self.USING_QDRANT:
            hits = self._qdrant.search(
                collection_name=settings.COLLECTION_NAME, 
                query_vector=vector, 
                limit=limit
            )
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.docs_memory:
                if query_text.lower() in doc.lower():
                    results.append(doc)
            
            if not results and self.docs_memory:
                results = [self.docs_memory[0]] # Just grab first
                
        return results

    def get_status(self) -> Dict[str, Any]:
        return {
            "qdrant_ready": self.USING_QDRANT,
            "in_memory_docs_count": len(self.docs_memory)
        }
