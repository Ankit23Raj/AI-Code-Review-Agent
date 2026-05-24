from fastapi import FastAPI

from app.api.webhook import router


# Create the FastAPI application for the webhook server.
app = FastAPI()

# Register the webhook router so GitHub events can reach the worker queue.
app.include_router(router)


@app.get("/health")
def health():
    # A small health check helps confirm the API is running.
    return {"status": "working"}