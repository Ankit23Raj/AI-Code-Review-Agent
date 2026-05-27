from app.reviewer.schemas import ReviewResult


def aggregate_findings(findings):
    if not findings:
        return ReviewResult(
            summary="No issues found.",
            findings=[],
            model_used="local-stub",
            duration_ms=0,
        )

    unique = []
    seen = set()

    for finding in findings:

        category = finding.get("category") if isinstance(finding, dict) else finding.category
        file_path = finding.get("file_path") if isinstance(finding, dict) else finding.file_path
        line_start = finding.get("line_start") if isinstance(finding, dict) else finding.line_start
        line_end = finding.get("line_end") if isinstance(finding, dict) else finding.line_end
        message = finding.get("message") if isinstance(finding, dict) else finding.message

        key = (
            category,
            file_path,
            line_start,
            line_end,
            message,
        )

        if key not in seen:
            seen.add(key)
            unique.append(finding)

    return ReviewResult(
        summary=f"Found {len(unique)} issue(s).",
        findings=unique,
        model_used="local-stub",
        duration_ms=0,
    )