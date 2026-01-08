from fastapi import FastAPI
from .config.config import settings
from .routes.router import router

app = FastAPI(title=settings.APP_TITLE)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
