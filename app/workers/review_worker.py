from app.workers.analyzer import analyze_code
import os
from redis import Redis
from rq import Queue

from app.github.github_client import (
    get_changed_files,
    get_file_content,
    post_pr_comment,
)

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
    print("Redis connected")
except Exception as e:
    print("Redis Error:", e)

queue = Queue(
    connection=redis_connection
)

try:
    print(
        "Queue status:",
        queue.name,
        "size=",
        queue.count
    )
except Exception as e:
    print("Queue status error:", e)

def process_review(payload):

    # This runs inside the RQ worker process when a queued job is picked up.
    print("Worker started")
    print("Job received")

    repository = payload.get(
        "repository",
        {}
    ).get(
        "full_name"
    )

    pr_number = payload.get(
        "pull_request",
        {}
    ).get(
        "number"
    )

    print(
        "Starting review..."
    )

    files = get_changed_files(
        repository,
        pr_number
    )

    for file in files:
        print("Processing review")

        # Review one changed file at a time so the output stays easy to follow.
        print(f"Reviewing: {file.filename}")

        # Fetch the latest file content from GitHub before running the checks.
        content = get_file_content(
            repository,
            file.filename,
        )

        # Run the modular analyzer and collect all findings.
        review = analyze_code(content)

        # Confirm we have analyzer output before trying to post a comment.
        print(
            "Analyzer output exists:",
            review is not None
        )
        print(
            "Analyzer findings count:",
            len(review["security"]) + len(review["quality"]) + len(review["best_practices"])
        )

        # Build a Markdown message that can be posted as a PR comment.
        review_message = [
            "## AI Review Result",
            "",
            "### Security",
        ]

        if review["security"]:
            review_message.extend(
                f"* {finding}" for finding in review["security"]
            )
        else:
            review_message.append("* No issues found")

        review_message.extend([
            "",
            "### Quality",
        ])

        if review["quality"]:
            review_message.extend(
                f"* {finding}" for finding in review["quality"]
            )
        else:
            review_message.append("* No issues found")

        review_message.extend([
            "",
            "### Best Practices",
        ])

        if review["best_practices"]:
            review_message.extend(
                f"* {finding}" for finding in review["best_practices"]
            )
        else:
            review_message.append("* No issues found")

        review_text = "\n".join(review_message)

        print("Security:")
        if review["security"]:
            for finding in review["security"]:
                print(f"* {finding}")
        else:
            print("* No security findings.")

        print("Quality:")
        if review["quality"]:
            for finding in review["quality"]:
                print(f"* {finding}")
        else:
            print("* No quality findings.")

        print("Best Practices:")
        if review["best_practices"]:
            for finding in review["best_practices"]:
                print(f"* {finding}")
        else:
            print("* No best practice findings.")

        print("")

        # Post the finished review back to the pull request as a GitHub comment.
        try:
            post_pr_comment(
                repository,
                pr_number,
                review_text,
            )
        except Exception as e:
            print("PR Comment Error:", e)
