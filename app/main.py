import os

from fastapi import FastAPI
from redis import Redis
from rq import Worker

from app.api.webhook import router


# Create the FastAPI application for the webhook server.
app = FastAPI()

# Register the webhook router so GitHub events can reach the worker queue.
app.include_router(router)


@app.get("/health")
def health():
    # A small health check helps confirm the API is running.
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_connection = Redis.from_url(redis_url)

    try:
        redis_connection.ping()
        redis_status = "connected"
        queue_status = "active"
        worker_status = "running" if Worker.all(connection=redis_connection) else "stopped"
    except Exception:
        redis_status = "disconnected"
        queue_status = "inactive"
        worker_status = "stopped"

    return {
        "status": "working",
        "redis": redis_status,
        "queue": queue_status,
        "worker": worker_status,
    }