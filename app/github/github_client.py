from github import Github
from app.config import GITHUB_TOKEN

github_client = Github(
    GITHUB_TOKEN
)

def get_repository(repo_name):

    return github_client.get_repo(
        repo_name
    )


def get_pull_request(
    repo_name,
    pr_number
):

    repo = get_repository(
        repo_name
    )

    return repo.get_pull(
        pr_number
    )


def get_changed_files(
    repo_name,
    pr_number
):

    pull_request = get_pull_request(
        repo_name,
        pr_number
    )

    return pull_request.get_files()


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

    return file.decoded_content.decode(
        "utf-8"
    )


def post_pr_comment(
    repo_name,
    pr_number,
    message
):
    # Load the repository object first so we can reach the pull request.
    repo = get_repository(
        repo_name
    )

    # Load the pull request that we want to comment on.
    pull_request = repo.get_pull(
        pr_number
    )

    # Add the review message as a normal PR comment.
    pull_request.create_issue_comment(
        message
    )