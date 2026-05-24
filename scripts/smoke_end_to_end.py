from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.parser.tree_parser import parse_file
from app.agents.security import run_security_agent
from app.agents.logic import run_logic_agent
from app.agents.style import run_style_agent
from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown

fixture_path = Path("tests/fixtures/sql_injection.py")
content = fixture_path.read_text()

facts = parse_file(str(fixture_path), content, changed_lines=None)

all_findings = []
all_findings.extend(run_security_agent(content))
all_findings.extend(run_logic_agent(content))
all_findings.extend(run_style_agent(content))

review = aggregate_findings(all_findings)
markdown = format_review_markdown(review)

print("FACTS:")
for fact in facts:
    print(fact)

print("\nREVIEW:")
print(markdown)