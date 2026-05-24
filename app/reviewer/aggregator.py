def aggregate_findings(findings):
    # findings is a list of dictionaries from security, logic, and style agents

    if not findings:
        return {
            "summary": "No issues found.",
            "findings": [],
            "model_used": "",
            "duration_ms": 0
        }

    return {
        "summary": f"Found {len(findings)} issue(s).",
        "findings": findings,
        "model_used": "local-stub",
        "duration_ms": 0
    }
