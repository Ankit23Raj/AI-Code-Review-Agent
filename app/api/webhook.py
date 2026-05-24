from fastapi import APIRouter
from app.github.github_client import (
    get_changed_files,
    get_file_content
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

        content = get_file_content(
            repository,
            file.filename
        )

        print(
            content[:200]
        )