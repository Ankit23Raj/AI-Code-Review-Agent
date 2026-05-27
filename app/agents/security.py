from app.agents.model_adapter import ask_model
from app.agents.response_utils import parse_agent_response
from app.rag.search import search_similar_code


def run_security_agent(context):
    findings = []

    query = {
        "file_path": "",
        "symbol_name": "",
        "snippet": context,
    }

    search_result = search_similar_code(query)
    best_match = search_result.get("best_match")

    extra_context = ""

    if best_match:
        extra_context = (
            f"\n\nSimilar code from repository:\n"
            f"{best_match.get('snippet', '')}\n"
        )

    prompt = f"""
You are a security code reviewer.

Analyze this Python code for:
- SQL Injection
- Hardcoded secrets
- Dangerous code patterns

Code:
{context}
{extra_context}

Return ONLY valid JSON with this schema:
{{
    "severity": "LOW | MEDIUM | HIGH",
    "category": "Security",
    "file_path": "",
    "line_start": 0,
    "line_end": 0,
    "message": "",
    "suggestion": "",
    "confidence": 0.0,
    "agent_name": "security"
}}
Do not explain anything outside JSON.
Do not use markdown or code fences.
"""

    response = ask_model(prompt)
    findings.append(
        parse_agent_response(
            response,
            category="Security",
            agent_name="security",
        )
    )

    return findings