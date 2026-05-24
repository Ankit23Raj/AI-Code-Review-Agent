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
        print(f"Reviewing: {file.filename}")

        content = get_file_content(
            repository,
            file.filename,
        )

        review = analyze_code(content)

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
