from app.agents.model_adapter import ask_model


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

    findings.append({
        "severity": "MEDIUM",
        "category": "AI Logic Review",
        "message": response,
        "suggestion": "Review the AI-generated findings",
        "agent_name": "logic"
    })

    return findings
