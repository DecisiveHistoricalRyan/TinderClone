import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.entrypoints.api import router

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    debug = settings.STAGE
    uvicorn.run("app.main:app", port=8082, reload=True)
