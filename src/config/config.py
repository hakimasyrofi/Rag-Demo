import os

class Settings:
    APP_TITLE = "Learning RAG Demo"
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    COLLECTION_NAME = "demo_collection"
    EMBEDDING_DIM = 128
    
settings = Settings()
