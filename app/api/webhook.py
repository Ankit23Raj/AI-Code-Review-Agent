from fastapi import APIRouter
from app.github.github_client import get_pull_request

router = APIRouter()

@router.post("/webhook")
async def github_webhook(payload: dict):

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

    if repository and pr_number:

        pr = get_pull_request(
            repository,
            pr_number
        )

        print(
            "PR Title:",
            pr.title
        )

        print(
            "PR State:",
            pr.state
        )

    return {
        "status":"success"
    }