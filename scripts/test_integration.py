from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.reviewer.review_pipeline import review_payload


payload = {
    "repo_path": "AI-Code-Review-Agent",
    "pr_number": 1,
    "changed_files": [
        {
            "file_path": "app/main.py",
            "content": "print('hello')",
        }
    ],
}


result = review_payload(payload)

findings_count = len(result.get("findings", []))

print(f"findings count: {findings_count}")
print(result.get("markdown", ""))