from github import Github
from app.config import GITHUB_TOKEN
from app.utils.logger import log

# This log helps confirm the token was loaded without exposing its value.
log(
    f"GitHub token loaded: {bool(GITHUB_TOKEN)}"
)

github_client = Github(
    GITHUB_TOKEN
)

def get_repository(repo_name):

    # Fetch the repository object from GitHub.
    repo = github_client.get_repo(
        repo_name
    )

    log("Repository fetch works")

    return repo


def get_pull_request(
    repo_name,
    pr_number
):

    repo = get_repository(
        repo_name
    )

    # Fetch the pull request so the worker can inspect the review target.
    pull_request = repo.get_pull(
        pr_number
    )

    log("Pull request fetch works")

    return pull_request


def get_changed_files(
    repo_name,
    pr_number
):

    pull_request = get_pull_request(
        repo_name,
        pr_number
    )

    changed_files = pull_request.get_files()

    log("Changed file retrieval works")

    return changed_files


def get_file_content(
    repo_name,
    file_path
):

    repo = get_repository(
        repo_name
    )

    file = repo.get_contents(
        file_path
    )

    log("File content retrieval works")

    return file.decoded_content.decode(
        "utf-8"
    )


def post_pr_comment(
    repo_name,
    pr_number,
    message
):
    try:
        # Load the repository object first so we can reach the pull request.
        repo = get_repository(
            repo_name
        )
        log(
            f"Repository object exists: {repo is not None}"
        )

        # Load the pull request that we want to comment on.
        pull_request = repo.get_pull(
            pr_number
        )
        log(
            f"PR object exists: {pull_request is not None}"
        )

        # Add the review message as a normal PR comment.
        log("Creating PR comment...")
        pull_request.create_issue_comment(
            message
        )
        log("Comment posted successfully")
    except Exception as e:
        log(f"PR Comment Error: {e}")