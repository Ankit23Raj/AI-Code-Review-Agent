"""Small review engine used by the background worker.

The checks stay intentionally simple so the code is easy to read and extend.
Each checker returns a list of human-readable findings.
"""

import re


def check_security(content):
    findings = []
    lower_content = content.lower()

    if "password" in lower_content:
        findings.append("Contains the word 'password'.")

    if "secret" in lower_content:
        findings.append("Contains the word 'secret'.")

    if "api_key" in lower_content:
        findings.append("Contains the word 'api_key'.")

    # Look for simple hardcoded credential patterns such as password = "...".
    credential_pattern = re.compile(
        r"\b(password|secret|api_key)\b\s*[:=]\s*['\"][^'\"]+['\"]",
        re.IGNORECASE,
    )
    if credential_pattern.search(content):
        findings.append("Possible hardcoded credential detected.")

    return findings


def check_code_quality(content):
    findings = []

    if "print(" in content:
        findings.append("Contains print statement(s).")

    if "TODO" in content:
        findings.append("Contains TODO comment(s).")

    if len(content) > 1000:
        findings.append("File is longer than 1000 characters.")

    return findings


def check_best_practices(content):
    findings = []

    # Check for lines that are longer than 100 characters.
    for line_number, line in enumerate(content.splitlines(), start=1):
        if len(line) > 100:
            findings.append(f"Line {line_number} is longer than 100 characters.")

    # Track duplicate imports with a very small, beginner-friendly parser.
    seen_imports = set()
    duplicate_imports = set()

    for line in content.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("import ") or stripped_line.startswith("from "):
            if stripped_line in seen_imports:
                duplicate_imports.add(stripped_line)
            else:
                seen_imports.add(stripped_line)

    for duplicate_import in sorted(duplicate_imports):
        findings.append(f"Duplicate import found: {duplicate_import}")

    return findings


def analyze_code(content):
    return {
        "security": check_security(content),
        "quality": check_code_quality(content),
        "best_practices": check_best_practices(content),
    }