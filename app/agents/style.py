from app.agents.model_adapter import ask_model


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

    findings.append({
        "severity": "LOW",
        "category": "AI Style Review",
        "message": response,
        "suggestion": "Review the AI-generated findings",
        "agent_name": "style"
    })

    return findings
