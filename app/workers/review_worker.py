from app.workers.analyzer import analyze_code
from redis import Redis
from rq import Queue

from app.github.github_client import (
    get_changed_files,
    get_file_content
)

redis_connection = Redis()

queue = Queue(
    connection=redis_connection
)

def process_review(payload):

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

        print(
            "Reviewing:",
            file.filename
        )

        content = get_file_content(
            repository,
            file.filename
        )

        print(
            review = analyze_code(
    content
)

print(
    "Review Result:"
)

for item in review:

    print("-", item)
        )
