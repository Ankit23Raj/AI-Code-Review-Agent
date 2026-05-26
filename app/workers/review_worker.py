import os
import time

# macOS needs this before RQ forks worker processes.
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

from redis import Redis
from rq import Queue

from app.utils.logger import log
from app.workers.analyzer import analyze_code
from app.storage.review_history import (
    append_review_history,
    build_review_history_record,
)

from app.github.github_client import (
    get_changed_files,
    get_file_content,
    post_pr_comment,
)


SEVERITY_BY_BUCKET = {
    "security": "HIGH",
    "quality": "MEDIUM",
    "best_practices": "LOW",
}

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

    repository = payload.get(
        "repository",
        {}
    ).get(
        "full_name"
    )

    pull_request_payload = payload.get(
        "pull_request",
        {}
    )

    pr_number = pull_request_payload.get(
        "number"
    )

    branch_name = pull_request_payload.get(
        "head",
        {}
    ).get(
        "ref"
    )

    log("Starting review...")

    files = get_changed_files(
        repository,
        pr_number
    )

    findings_by_bucket = {
        "security": [],
        "quality": [],
        "best_practices": [],
    }
    files_reviewed = 0

    for file in files:
        log("Processing review")

        # Review one changed file at a time so the output stays easy to follow.
        log(f"Reviewing: {file.filename}")

        # Fetch the latest file content from GitHub before running the checks.
        content = get_file_content(
            repository,
            file.filename,
            branch_name,
        )

        # Skip files that cannot be safely decoded, like binary files.
        if content is None:
            log(f"Skipping unreadable file: {file.filename}")
            continue

        files_reviewed += 1

        # Run the modular analyzer and collect all findings.
        review = analyze_code(content)

        # Confirm we have analyzer output before trying to post a comment.
        log(f"Analyzer output exists: {review is not None}")
        log(
            "Analyzer findings count: "
            f"{len(review['security']) + len(review['quality']) + len(review['best_practices'])}"
        )

        for bucket in findings_by_bucket:
            findings_by_bucket[bucket].extend(review[bucket])

    total_findings = sum(
        len(findings)
        for findings in findings_by_bucket.values()
    )

    high_count = len(findings_by_bucket["security"])
    medium_count = len(findings_by_bucket["quality"])
    low_count = len(findings_by_bucket["best_practices"])
    processing_time = round(time.time() - start_time, 2)

    review_message = [
        "## AI Review Summary",
        "",
        "### Review Statistics",
        f"Files reviewed: {files_reviewed}",
        f"Total findings: {total_findings}",
        f"HIGH: {high_count}",
        f"MEDIUM: {medium_count}",
        f"LOW: {low_count}",
        f"Processing Time: {processing_time} sec",
        "",
    ]

    for bucket in ("security", "quality", "best_practices"):
        bucket_findings = findings_by_bucket[bucket]
        if not bucket_findings:
            continue

        review_message.append(f"### {bucket.replace('_', ' ').title()}")
        review_message.extend(
            f"* {SEVERITY_BY_BUCKET[bucket]}: {finding}"
            for finding in bucket_findings
        )
        review_message.append("")

    if total_findings == 0:
        review_message.extend([
            "No issues found.",
            "",
        ])

    review_text = "\n".join(review_message)

    log("Security:")
    if findings_by_bucket["security"]:
        for finding in findings_by_bucket["security"]:
            log(f"* {finding}")
    else:
        log("* No security findings.")

    log("Quality:")
    if findings_by_bucket["quality"]:
        for finding in findings_by_bucket["quality"]:
            log(f"* {finding}")
    else:
        log("* No quality findings.")

    log("Best Practices:")
    if findings_by_bucket["best_practices"]:
        for finding in findings_by_bucket["best_practices"]:
            log(f"* {finding}")
    else:
        log("* No best practice findings.")

    log("")

    append_review_history(
        build_review_history_record(
            repository=repository,
            pr_number=pr_number,
            files_reviewed=files_reviewed,
            findings_count=total_findings,
        )
    )

    # Post the finished review back to the pull request as a GitHub comment.
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

    log("Review completed")
