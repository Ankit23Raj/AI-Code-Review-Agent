def run_style_agent(context):
    findings = []

    if "badFunctionName" in context:
        findings.append({
            "severity": "LOW",
            "category": "Style Issue",
            "message": "Non-PEP8 function name detected",
            "suggestion": "Use snake_case for function names",
            "agent_name": "style"
        })

    return findings
