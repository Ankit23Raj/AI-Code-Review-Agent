from app.workers.review_worker import queue
from fastapi import APIRouter

router = APIRouter()

@router.post("/webhook")
async def github_webhook(payload: dict):

    # Log the webhook payload details so we can confirm GitHub reached FastAPI.
    print("Webhook received")
    print(
        "Repository name:",
        payload.get("repository", {}).get("full_name")
    )
    print(
        "PR number:",
        payload.get("pull_request", {}).get("number")
    )

    # Push the review job into Redis so the RQ worker can process it.
    job = queue.enqueue(
        "app.workers.review_worker.process_review",
        payload
    )

    # Confirm that the enqueue step really happened.
    print(
        "queue.enqueue() executed",
        job.id
    )

    return {
        "status":"Review job queued"
    }