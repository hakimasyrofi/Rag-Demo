import random
from typing import List
from ..config.config import settings

class EmbeddingService:
    # Pretend this is a real embedding model
    def fake_embed(self, text: str) -> List[float]:
        # Seed based on input so it's "deterministic"
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(settings.EMBEDDING_DIM)] # Small vector for demo
