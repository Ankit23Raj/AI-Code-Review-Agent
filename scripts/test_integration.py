from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.parser.tree_parser import parse_file
from app.agents.security import run_security_agent
from app.agents.logic import run_logic_agent
from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown


fixture_path = Path("tests/fixtures/sql_injection.py")
content = fixture_path.read_text(encoding="utf-8")

print(f"Reviewing: {fixture_path}")

code_facts = parse_file(str(fixture_path), content, [])

for fact in code_facts:
    print("FACT:")
    print(fact)

security_findings = run_security_agent(content)
logic_findings = run_logic_agent(content)

findings = security_findings + logic_findings

review = aggregate_findings(findings)

formatted_review = format_review_markdown(review)

print("\nFINAL REVIEW:\n")
print(formatted_review)