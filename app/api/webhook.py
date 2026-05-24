from fastapi import APIRouter
from app.github.github_client import get_changed_files

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

        files = get_changed_files(
            repository,
            pr_number
        )

        for file in files:

            print(
                "Changed file:",
                file.filename
            )

    return {
        "status":"success"
    }