from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .embedding_service import EmbeddingService
from .storage_service import StorageService

class RagService:
    def __init__(self, embedding_service: EmbeddingService, storage_service: StorageService):
        self.embedding_service = embedding_service
        self.storage_service = storage_service
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def _retrieve(self, state: Dict[str, Any]):
        query = state["question"]
        emb = self.embedding_service.fake_embed(query)
        results = self.storage_service.search(vector=emb, query_text=query, limit=2)
        state["context"] = results
        return state

    def _answer(self, state: Dict[str, Any]):
        ctx = state.get("context", [])
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state

    def ask(self, question: str) -> Dict[str, Any]:
        result = self.workflow.invoke({"question": question})
        return result
