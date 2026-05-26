import json
from datetime import datetime, timezone
from pathlib import Path

from app.utils.logger import log


HISTORY_FILE = Path(__file__).with_name("review_history.json")


def append_review_history(record):
    try:
        if not HISTORY_FILE.exists():
            HISTORY_FILE.write_text("[]", encoding="utf-8")

        with HISTORY_FILE.open("r", encoding="utf-8") as file_handle:
            history = json.load(file_handle)

        if not isinstance(history, list):
            history = []

        history.append(record)

        with HISTORY_FILE.open("w", encoding="utf-8") as file_handle:
            json.dump(history, file_handle, indent=2)
    except Exception as e:
        log(f"Review history write failed: {e}", level="ERROR")


def build_review_history_record(
    repository,
    pr_number,
    files_reviewed,
    findings_count,
):
    return {
        "repository": repository,
        "pr_number": pr_number,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files_reviewed": files_reviewed,
        "findings_count": findings_count,
    }