from github import Github
from app.config import GITHUB_TOKEN

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

    # Pull the file list from the pull request.
    pull_request = get_pull_request(
        repo_name,
        pr_number
    )

    return pull_request.get_files()


def get_file_content(
    repo_name,
    file_path
):

    # Load the file contents directly from GitHub.
    repo = get_repository(
        repo_name
    )

    file = repo.get_contents(file_path)

    return file.decoded_content.decode("utf-8")


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
        print("Repository object exists:", repo is not None)

        # Load the pull request that we want to comment on.
        pull_request = repo.get_pull(
            pr_number
        )
        print("PR object exists:", pull_request is not None)

        # Add the review message as a normal PR comment.
        print("Creating PR comment...")
        pull_request.create_issue_comment(message)
        print("Comment posted successfully")
    except Exception as e:
        print("PR Comment Error:", e)