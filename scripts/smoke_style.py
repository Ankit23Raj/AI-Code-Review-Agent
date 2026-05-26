from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agents.style import run_style_agent

fixture_path = Path("tests/fixtures/style_issue.py")
content = fixture_path.read_text()

findings = run_style_agent(content)

for finding in findings:
    print(finding)
