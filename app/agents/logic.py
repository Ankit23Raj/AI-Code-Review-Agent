def run_logic_agent(context):
    findings = []

    text = context.lower()

    if "return a / b" in text or "divide(" in text:
        findings.append({
            "severity": "MEDIUM",
            "category": "Logic Issue",
            "message": "Potential unsafe division without validation",
            "suggestion": "Check for zero before dividing",
            "agent_name": "logic"
        })

    return findings
