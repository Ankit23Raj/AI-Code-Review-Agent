from app.reviewer.schemas import Finding


def run_security_agent(code_fact):
    prompt = f"""
You are a security code reviewer.

Analyze this Python function for:
- SQL injection
- hardcoded secrets
- unsafe input handling
- dangerous eval/exec usage

Function Name:
{code_fact.symbol_name}

Code:
{code_fact.snippet}

Imports:
{code_fact.imports}

String Literals:
{code_fact.literals}

Return:
- severity
- issue
- explanation
- fix suggestion
"""

    print(prompt)

    return Finding(
        severity="high",
        category="security",
        file_path=code_fact.file_path,
        line_start=code_fact.start_line,
        line_end=code_fact.end_line,
        message="Possible SQL injection",
        suggestion="Use parameterized queries instead of string concatenation.",
        confidence=0.92,
        agent_name="security_agent",
    )


class FakeCodeFact:
    file_path = "auth.py"
    symbol_name = "login_user"
    start_line = 10
    end_line = 15

    snippet = """
def login_user(username, password):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return query
"""

    imports = ["sqlite3"]

    literals = ['"SELECT * FROM users WHERE name = \'"']


if __name__ == "__main__":
    result = run_security_agent(FakeCodeFact())
    print(result)