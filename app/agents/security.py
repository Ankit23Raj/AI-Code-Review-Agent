from app.agents.model_adapter import ask_model
from app.reviewer.schemas import Finding
from app.rag.search import search_similar_code

def run_security_agent(context):
    findings = []

    query = {
        "file_path": "",
        "symbol_name": "",
        "snippet": context
    }

    search_result = search_similar_code(query)
    best_match = search_result.get("best_match")
    extra_context = ""
    if best_match:
        extra_context = f"\n\nSimilar code from repository:\n{best_match.get('snippet', '')}\n"

    prompt = f"""
You are a security code reviewer.

Analyze this Python code for:
- SQL Injection
- Hardcoded secrets
- Dangerous code patterns

Code:
{context}{extra_context}

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