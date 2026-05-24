from app.agents.model_adapter import ask_model
from app.reviewer.schemas import Finding


def run_logic_agent(context):
    findings = []

    prompt = f"""
You are a logic code reviewer.

Analyze this Python code for:
- unsafe division
- missing validation
- missing error handling
- possible runtime bugs
- bad control flow

Code:
{context}

Respond briefly with detected issues.
"""

    response = ask_model(prompt)

    findings.append(
        Finding(
            severity="MEDIUM",
            category="AI Logic Review",
            file_path="",
            line_start=0,
            line_end=0,
            message=response,
            suggestion="Review the AI-generated findings",
            confidence=0.8,
            agent_name="logic",
        )
    )

    return findings
