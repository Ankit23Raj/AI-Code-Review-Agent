from app.agents.model_adapter import ask_model
from app.reviewer.schemas import Finding


def run_style_agent(context):
    findings = []

    prompt = f"""
You are a Python style reviewer.

Analyze this Python code for:
- PEP8 violations
- bad naming conventions
- poor formatting
- readability problems
- maintainability issues

Code:
{context}

Respond briefly with detected issues.
"""

    response = ask_model(prompt)

    findings.append(
        Finding(
            severity="LOW",
            category="AI Style Review",
            file_path="",
            line_start=0,
            line_end=0,
            message=response,
            suggestion="Review the AI-generated findings",
            confidence=0.8,
            agent_name="style",
        )
    )

    return findings
