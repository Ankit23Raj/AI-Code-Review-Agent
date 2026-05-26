from fastapi import APIRouter

from app.workers.review_worker import queue
from app.utils.logger import log

router = APIRouter()


@router.post("/webhook")
async def github_webhook(payload: dict):

    # Read the repository and PR number safely from the incoming payload.
    repository = payload.get("repository", {}).get("full_name")
    pr_number = payload.get("pull_request", {}).get("number")

    log("Webhook received")
    log(f"Repository: {repository}")
    log(f"PR number: {pr_number}")

    # Push the review job into Redis so the RQ worker can process it.
    job = queue.enqueue(
        "app.workers.review_worker.process_review",
        payload
    )

    # Confirm the job was accepted by the queue.
    log(f"queue.enqueue() executed: {job.id}")

    return {"status": "Job added"}