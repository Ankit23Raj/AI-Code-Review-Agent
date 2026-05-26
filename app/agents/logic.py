import json
import re

from app.agents.model_adapter import ask_model
from app.reviewer.schemas import Finding
from app.rag.search import search_similar_code


def run_logic_agent(context):
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
You are a logic code reviewer.

Analyze this Python code for:
- unsafe division
- missing validation
- missing error handling
- possible runtime bugs
- bad control flow

Code:
{context}
{extra_context}

Return ONLY valid JSON.
Do not explain anything outside JSON.
Do not use markdown.
Do not use triple backticks.
"""

    response = ask_model(prompt)

    cleaned = response.strip()
    cleaned = cleaned.replace("\n", " ").replace("\r", " ")
    cleaned = re.sub(r"```json", "", cleaned)
    cleaned = re.sub(r"```", "", cleaned)

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    candidate = match.group(0) if match else cleaned

    try:
        payload = json.loads(candidate, strict=False)

        message = ""

        if isinstance(payload, dict):

            if "errors" in payload and isinstance(payload["errors"], list):
                errors = payload["errors"]

                if errors and isinstance(errors[0], dict):
                    message = ", ".join(
                        error.get("message", "")
                        for error in errors
                    )

                elif errors and isinstance(errors[0], str):
                    message = ", ".join(errors)

                else:
                    message = str(errors)

            elif "message" in payload:
                message = payload.get("message", "")

            else:
                message = ", ".join(
                    key.replace("_", " ")
                    for key, value in payload.items()
                    if value is True
                )

                if not message:
                    message = str(payload)

        else:
            message = str(payload)

        findings.append(
            Finding(
                severity=payload.get("severity", "LOW"),
                category=payload.get("category", "AI Logic Review"),
                file_path="",
                line_start=0,
                line_end=0,
                message=message,
                suggestion=payload.get(
                    "suggestion",
                    "Review the AI-generated findings",
                ),
                confidence=payload.get("confidence", 0.8),
                agent_name="logic",
            )
        )
 
    except (json.JSONDecodeError, TypeError, ValueError):

        findings.append(
            Finding(
                severity="LOW",
                category="Parsing Error",
                file_path="",
                line_start=0,
                line_end=0,
                message="Failed to parse AI response",
                suggestion="Check model output formatting",
                confidence=0.0,
                agent_name="logic",
            )
        )

    return findings