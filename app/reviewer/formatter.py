def _get_value(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)

def format_review_markdown(review):
    lines = []

    lines.append("# Review Summary\n")
    lines.append(f"{_get_value(review, 'summary', 'No summary available')}\n")

    findings = _get_value(review,"findings", [])

    if not findings:
        lines.append("## No issues found\n")
        return "\n".join(lines)

    lines.append("## Findings\n")

    for finding in findings:
        lines.append(
            f"### {_get_value(finding, 'severity', 'INFO')} - {_get_value(finding, 'category', 'General')}"
        )
        lines.append(f"- Message: {_get_value(finding, 'message', '')}")
        lines.append(f"- Suggestion: {_get_value(finding, 'suggestion', '')}")
        lines.append(f"- Agent: {_get_value(finding, 'agent_name', '')}")
        lines.append("")

    return "\n".join(lines)