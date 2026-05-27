import os
import time

# macOS needs this before RQ forks worker processes.
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

from redis import Redis
from rq import Queue

from app.reviewer.review_pipeline import review_payload
from app.utils.logger import log
from app.storage.review_history import (
    append_review_history,
    build_review_history_record,
)

from app.github.github_client import post_pr_comment

redis_url = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

# Build the Redis connection once so both the API and worker use the same queue.
redis_connection = Redis.from_url(
    redis_url
)

try:
    # Ping Redis so we know the worker can talk to the queue backend.
    redis_connection.ping()
    log("Redis connected")
except Exception as e:
    log(f"Redis Error: {e}")

queue = Queue(
    connection=redis_connection
)

try:
    log(
        f"Queue status: {queue.name} size={queue.count}"
    )
except Exception as e:
    log(f"Queue status error: {e}")
def process_review(payload):

    # This runs inside the RQ worker process when a queued job is picked up.
    start_time = time.time()
    log("Worker started")
    log("Job received")

    try:
        result = review_payload(payload)

        repository = result.get("repo_path") or payload.get("repository", {}).get("full_name") or payload.get("repo_path")
        pr_number = result.get("pr_number") or payload.get("pull_request", {}).get("number") or payload.get("pr_number")
        review_text = result.get("markdown", "")
        findings = result.get("findings", [])
        findings_count = len(findings)
        files_reviewed = result.get("files_reviewed", len(payload.get("changed_files", [])))

        append_review_history(
            build_review_history_record(
                repository=repository,
                pr_number=pr_number,
                files_reviewed=files_reviewed,
                findings_count=findings_count,
            )
        )

        try:
            posted = post_pr_comment(
                repository,
                pr_number,
                review_text,
            )
            if not posted:
                log("Review summary comment already exists; skipped posting")
        except Exception as e:
            log(f"PR Comment Error: {e}", level="ERROR")

        processing_time = round(time.time() - start_time, 2)
        log(f"Review completed in {processing_time} sec")

        return {
            "findings": findings,
            "review_text": review_text,
            "counts": {
                "total": findings_count,
            },
        }
    except Exception as e:
        log("Failed to process payload", level="ERROR")
        log(f"{e}", level="ERROR")
        raise
