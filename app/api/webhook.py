from fastapi import APIRouter

from app.workers.review_worker import queue
from app.utils.logger import log

router = APIRouter()


@router.post("/webhook")
async def github_webhook(payload: dict):
    job = queue.enqueue(
        "app.workers.review_worker.process_review",
        payload
    )

    log(f"queue.enqueue() executed: {job.id}")

    return {"status": "Job added"}