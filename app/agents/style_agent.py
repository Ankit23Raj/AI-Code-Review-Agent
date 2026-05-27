from app.reviewer.schemas import Finding


def run_style_agent(code_fact):
    prompt = f"""
You are a Python style and readability reviewer.

Analyze this function for:
- poor variable names
- bad readability
- very long functions
- duplicated code
- bad formatting
- missing comments/docstrings
- Python best practice violations

Function Name:
{code_fact.symbol_name}

Code:
{code_fact.snippet}

Return:
- severity
- issue
- explanation
- fix suggestion
"""

    print(prompt)

    return Finding(
        severity="LOW",
        category="Style",
        file_path=code_fact.file_path,
        line_start=code_fact.start_line,
        line_end=code_fact.end_line,
        message="Function readability can be improved.",
        suggestion="Use clearer variable names and split large logic into smaller functions.",
        confidence=0.75,
        agent_name="style_agent",
    )


class FakeCodeFact:
    file_path = "utils.py"
    symbol_name = "x"
    start_line = 1
    end_line = 12

    snippet = """
def x(a,b,c,d,e):
    temp=a+b+c+d+e
    return temp
"""


if __name__ == "__main__":
    result = run_style_agent(FakeCodeFact())
    print(result)