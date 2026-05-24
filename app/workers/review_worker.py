from app.workers.analyzer import analyze_code
from redis import Redis
from rq import Queue

from app.github.github_client import (
    get_changed_files,
    get_file_content,
    post_pr_comment,
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
        # Review one changed file at a time so the output stays easy to follow.
        print(f"Reviewing: {file.filename}")

        # Fetch the latest file content from GitHub before running the checks.
        content = get_file_content(
            repository,
            file.filename,
        )

        # Run the modular analyzer and collect all findings.
        review = analyze_code(content)

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
        post_pr_comment(
            repository,
            pr_number,
            review_text,
        )
