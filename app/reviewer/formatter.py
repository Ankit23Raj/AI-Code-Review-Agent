def format_review_markdown(review):
    lines = []

    lines.append(f"# Review Summary\n")
    lines.append(f"{review.get('summary', 'No summary available')}\n")

    findings = review.get("findings", [])

    if not findings:
        lines.append("## No issues found\n")
        return "\n".join(lines)

    lines.append("## Findings\n")

    for finding in findings:
        lines.append(
            f"### {finding.get('severity', 'INFO')} - {finding.get('category', 'General')}"
        )
        lines.append(f"- Message: {finding.get('message', '')}")
        lines.append(f"- Suggestion: {finding.get('suggestion', '')}")
        lines.append(f"- Agent: {finding.get('agent_name', '')}")
        lines.append("")

    return "\n".join(lines)
