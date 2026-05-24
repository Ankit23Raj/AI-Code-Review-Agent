def run_security_agent(context):
    findings = []

    text = context.lower()

    # hardcoded secret check
    if "sk-" in text or "api_key" in text or "secret" in text:
        findings.append({
            "severity": "HIGH",
            "category": "Hardcoded Secret",
            "message": "Potential hardcoded API key or secret detected",
            "suggestion": "Move secrets to environment variables",
            "agent_name": "security"
        })

    # SQL injection check
    if "select" in text and "+" in text and "where" in text:
        findings.append({
            "severity": "HIGH",
            "category": "SQL Injection",
            "message": "Potential SQL injection vulnerability detected",
            "suggestion": "Use parameterized queries instead of string concatenation",
            "agent_name": "security"
        })

    return findings