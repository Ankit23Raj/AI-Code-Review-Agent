from app.agents.model_adapter import ask_model

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

    findings.append({
        "severity": "HIGH",
        "category": "AI Security Review",
        "message": response,
        "suggestion": "Review the AI-generated findings",
        "agent_name": "security"
    })

    return findings