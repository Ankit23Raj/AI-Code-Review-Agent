from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agents.logic import run_logic_agent

fixture_path = Path("tests/fixtures/logic_bug.py")
content = fixture_path.read_text()

findings = run_logic_agent(content)

for finding in findings:
    print(finding)
