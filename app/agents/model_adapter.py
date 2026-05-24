import subprocess

def ask_model(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "qwen2.5-coder:1.5b", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout.strip()