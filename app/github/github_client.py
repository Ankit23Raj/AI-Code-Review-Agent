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