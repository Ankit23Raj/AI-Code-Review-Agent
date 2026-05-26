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
        key = (
            finding.category,
            finding.file_path,
            finding.line_start,
            finding.line_end,
            finding.message,
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