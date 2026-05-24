from fastapi import FastAPI
from app.api.webhook import router
from app.config import GITHUB_TOKEN

app = FastAPI()



app.include_router(router)

@app.get("/health")
def health():
    return {"status":"working"}