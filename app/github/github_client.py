import os

from github import Github
from app.config import GITHUB_TOKEN
from app.utils.logger import log

github_client = Github(
    GITHUB_TOKEN
)


def get_repository(repo_name):

    # Fetch the repository object from GitHub.
    return github_client.get_repo(repo_name)


def get_pull_request(
    repo_name,
    pr_number
):

    # Get the repository first, then fetch the pull request from it.
    repo = get_repository(
        repo_name
    )

    return repo.get_pull(pr_number)


def get_changed_files(
    repo_name,
    pr_number
):

    # Pull the file list from the pull request and fetch safe text content only.
    pull_request = get_pull_request(
        repo_name,
        pr_number
    )

    changed_files = []

    for file in pull_request.get_files():
        file_path = getattr(file, "filename", None)
        if not file_path:
            continue

        if getattr(file, "status", None) == "removed":
            log(f"Skipping removed file: {file_path}")
            continue

        content = get_file_content(
            repo_name,
            file_path,
            getattr(getattr(pull_request, "head", None), "ref", None),
        )

        if content is None:
            log(f"Skipping unreadable or binary file: {file_path}")
            continue

        changed_files.append({
            "file_path": file_path,
            "content": content,
        })

    return changed_files


def get_file_content(
    repo_name,
    file_path,
    branch_name=None
):

    # Load the file contents directly from GitHub.
    if os.path.basename(file_path) == ".DS_Store" or file_path.endswith(".DS_Store"):
        return None

    repo = get_repository(
        repo_name
    )

    try:
        log(f"Fetching file: {file_path}")
        if branch_name:
            file = repo.get_contents(file_path, ref=branch_name)
        else:
            file = repo.get_contents(file_path)

        log("Fetched successfully")

        # Some files are binary or not safe to decode as UTF-8.
        return file.decoded_content.decode("utf-8")

    except UnicodeDecodeError:
        return None

    except Exception as e:
        log(f"File read error: {e}", level="ERROR")
        return None


def comment_already_exists(pull_request, message):
    try:
        target_body = message.strip()
        for comment in pull_request.get_issue_comments():
            if (comment.body or "").strip() == target_body:
                return True
    except Exception as e:
        log(f"Duplicate comment check failed: {e}", level="ERROR")

    return False


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
        log(f"Repository object exists: {repo is not None}")

        # Load the pull request that we want to comment on.
        pull_request = repo.get_pull(
            pr_number
        )
        log(f"PR object exists: {pull_request is not None}")

        if comment_already_exists(pull_request, message):
            log("Duplicate PR summary found; skipping comment")
            return False

        # Add the review message as a normal PR comment.
        log("Creating PR comment...")
        pull_request.create_issue_comment(message)
        log("Comment posted successfully")
        return True
    except Exception as e:
        log(f"PR Comment Error: {e}", level="ERROR")
        return False