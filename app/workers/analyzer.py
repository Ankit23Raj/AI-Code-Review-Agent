"""Small review engine used by the background worker.

The checks stay intentionally simple so the code is easy to read and extend.
Each checker returns a list of human-readable findings.
"""

import re


def iter_code_lines(content):
    in_docstring = False

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        if "\"\"\"" in stripped or "'''" in stripped:
            quote_count = stripped.count("\"\"\"") + stripped.count("'''")
            if quote_count % 2 == 1:
                in_docstring = not in_docstring
            continue

        if in_docstring:
            continue

        if "#" in line:
            line = line.split("#", 1)[0]

        if line.strip():
            yield line


def check_security(content):
    findings = []

    credential_pattern = re.compile(
        r"\b(api_key|password|secret|token)\b\s*[:=]\s*(?:['\"][^'\"]+['\"]|[^\s,]+)",
        re.IGNORECASE,
    )

    for line in iter_code_lines(content):
        if credential_pattern.search(line):
            findings.append("Hardcoded credential detected.")
            break

    return findings


def check_code_quality(content):
    findings = []

    for line in iter_code_lines(content):
        if "logger.info(" in line or "logger.debug(" in line:
            continue

        if re.search(r"(?<!\w)print\s*\(", line):
            findings.append("Print statement found.")
            break

    if "TODO" in content:
        findings.append("TODO comment found.")

    if len(content) > 2000:
        findings.append("Large file size.")

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