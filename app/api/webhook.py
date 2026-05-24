from app.workers.review_worker import queue
from fastapi import APIRouter

router = APIRouter()

@router.post("/webhook")
async def github_webhook(payload: dict):

    queue.enqueue(
        "app.workers.review_worker.process_review",
        payload
    )

    return {
        "status":"Review job queued"
    }