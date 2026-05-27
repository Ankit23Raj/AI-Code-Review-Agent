def format_review_markdown(review):

    markdown = "# AI Review Summary\n\n"

    markdown += f"{review.summary}\n\n"

    markdown += "## Findings\n\n"

    for finding in review.findings:

        severity = finding.get("severity", "INFO")
        category = finding.get("category", "General")
        message = finding.get("message", "")
        suggestion = finding.get("suggestion", "")

        markdown += f"### {severity} — {category}\n"

        markdown += f"**Issue:** {message}\n\n"

        if suggestion:
            markdown += f"**Suggestion:** {suggestion}\n\n"

        markdown += "---\n\n"

    markdown += f"Files reviewed: 1\n"
    markdown += f"Total findings: {len(review.findings)}\n"

    return markdown