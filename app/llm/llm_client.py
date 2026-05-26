import os
from typing import Optional

import ollama

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")


def generate_review(prompt: str, model: Optional[str] = None) -> str:
    model_name = model or DEFAULT_MODEL

    try:
        print("[llm_client] sending request...")
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        print("[llm_client] sending request...")

        return response["message"]["content"].strip()

    except Exception as e:
        print(f"[llm_client] Error while generating review: {e}")
        return ""


if __name__ == "__main__":
    sample_prompt = sample_prompt = """
You are an expert AI code reviewer.

Analyze the following Python function.

IMPORTANT:
Return ONLY valid JSON.
Do not explain anything outside JSON.
Do not use markdown.
Do not use triple backticks.

JSON format:

{
  "severity": "low|medium|high|critical",
  "category": "security|logic|style",
  "issue": "short issue title",
  "explanation": "clear explanation",
  "suggestion": "fix suggestion"
}

Code:
def login_user(username, password):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return query
"""

    result = generate_review(sample_prompt)
    print(result)