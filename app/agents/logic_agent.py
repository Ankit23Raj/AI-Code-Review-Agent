from app.reviewer.schemas import Finding


def run_logic_agent(code_fact):
    prompt = f"""
You are a logic code reviewer.

Analyze this Python function for:
- incorrect conditions
- edge cases
- bad control flow
- missing error handling
- wrong assumptions

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
        severity="medium",
        category="logic",
        file_path=code_fact.file_path,
        line_start=code_fact.start_line,
        line_end=code_fact.end_line,
        message="Possible logic issue",
        suggestion="Review the condition and edge cases carefully.",
        confidence=0.80,
        agent_name="logic_agent",
    )


class FakeCodeFact:
    file_path = "sample.py"
    symbol_name = "check_age"
    start_line = 5
    end_line = 10
    snippet = """
def check_age(age):
    if age > 18:
        return True
    return False
"""


if __name__ == "__main__":
    result = run_logic_agent(FakeCodeFact())
    print(result)