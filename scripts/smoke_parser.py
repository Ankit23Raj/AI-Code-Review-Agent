from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.parser.tree_parser import parse_file

fixture_path = Path("tests/fixtures/sql_injection.py")
content = fixture_path.read_text()

facts = parse_file(str(fixture_path), content, changed_lines=None)

for fact in facts:
    print(fact)