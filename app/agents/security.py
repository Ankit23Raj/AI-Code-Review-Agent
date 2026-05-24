from app.agents.model_adapter import ask_model
from app.reviewer.schemas import Finding

def run_security_agent(context):
    findings = []

    prompt = f"""
You are a security code reviewer.

Analyze this Python code for:
- SQL Injection
- Hardcoded secrets
- Dangerous code patterns

Code:
{context}

Respond briefly with detected issues.
"""

    response = ask_model(prompt)

    findings.append(
        Finding(
            severity="HIGH",
            category="AI Security Review",
            file_path="",
            line_start=0,
            line_end=0,
            message=response,
            suggestion="Review the AI-generated findings",
            confidence=0.8,
            agent_name="security",
        )
    )

    return findings