from app.utils.text_cleaner import clean_text


def _get_value(finding, key, default=None):
    if isinstance(finding, dict):
        return finding.get(key, default)
    return getattr(finding, key, default)


def format_review_markdown(review):

    markdown = "# AI Review Summary\n\n"

    markdown += f"{clean_text(getattr(review, 'summary', ''))}\n\n"

    markdown += "## Findings\n\n"

    for finding in review.findings:

        severity = _get_value(finding, "severity", "INFO")
        category = _get_value(finding, "category", "General")
        message = clean_text(_get_value(finding, "message", ""))
        suggestion = clean_text(_get_value(finding, "suggestion", ""))

        markdown += f"### {severity} — {category}\n"

        markdown += f"**Issue:** {message}\n\n"

        if suggestion:
            markdown += f"**Suggestion:** {suggestion}\n\n"

        markdown += "---\n\n"

    markdown += f"Files reviewed: 1\n"
    markdown += f"Total findings: {len(review.findings)}\n"

    return markdown