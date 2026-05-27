import os
import subprocess

def ask_model(prompt: str) -> str:
    model_name = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")
    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout.strip()