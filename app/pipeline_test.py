from app.reviewer.formatter import format_review_markdown
from app.parser.parser import parse_file
from app.agents.security_agent import run_security_agent
from app.agents.logic_agent import run_logic_agent
from app.agents.style_agent import run_style_agent
from app.reviewer.aggregator import aggregate_findings


sample = """
import sqlite3

def login_user(username, password):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return query
"""


if __name__ == "__main__":
    code_facts = parse_file("auth.py", sample, changed_lines=[4, 5])

    all_findings = []

    for code_fact in code_facts:
        all_findings.append(run_security_agent(code_fact))
        all_findings.append(run_logic_agent(code_fact))
        all_findings.append(run_style_agent(code_fact))

    result = aggregate_findings(all_findings)
    print(result)
    markdown = format_review_markdown(result)
print(markdown)