from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.reviewer.formatter import format_review_markdown

sample_review = {
    "summary": "Found 2 issue(s).",
    "findings": [
        {
            "severity": "HIGH",
            "category": "Hardcoded Secret",
            "message": "Potential hardcoded API key detected",
            "suggestion": "Move secrets to environment variables",
            "agent_name": "security"
        },
        {
            "severity": "LOW",
            "category": "Style Issue",
            "message": "Non-PEP8 function name detected",
            "suggestion": "Use snake_case for function names",
            "agent_name": "style"
        }
    ]
}

print(format_review_markdown(sample_review))
