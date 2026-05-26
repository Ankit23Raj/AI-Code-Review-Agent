from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.reviewer.aggregator import aggregate_findings

sample_findings = [
    {
        "severity": "HIGH",
        "category": "Hardcoded Secret",
        "message": "Potential hardcoded API key detected",
        "agent_name": "security"
    },
    {
        "severity": "LOW",
        "category": "Style Issue",
        "message": "Non-PEP8 function name detected",
        "agent_name": "style"
    }
]

result = aggregate_findings(sample_findings)

print(result)
