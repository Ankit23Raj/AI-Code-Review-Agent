from app.reviewer.schemas import ReviewResult
from app.utils.text_cleaner import clean_text


def _get_value(finding, key, default=None):
    if isinstance(finding, dict):
        return finding.get(key, default)
    return getattr(finding, key, default)


def _normalize_finding(finding):
    message = clean_text(_get_value(finding, "message", ""))
    if not message:
        return None

    suggestion = clean_text(_get_value(finding, "suggestion", ""))
    severity = _get_value(finding, "severity", "LOW")
    category = _get_value(finding, "category", "System")
    file_path = _get_value(finding, "file_path", "")
    line_start = _get_value(finding, "line_start", 0)
    line_end = _get_value(finding, "line_end", 0)
    confidence = _get_value(finding, "confidence", 0.0)
    agent_name = _get_value(finding, "agent_name", "")

    return {
        "severity": severity,
        "category": category,
        "file_path": file_path,
        "line_start": int(line_start) if str(line_start).isdigit() else 0,
        "line_end": int(line_end) if str(line_end).isdigit() else 0,
        "message": message,
        "suggestion": suggestion,
        "confidence": confidence,
        "agent_name": agent_name,
    }


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
        normalized = _normalize_finding(finding)
        if not normalized:
            continue

        key = (
            normalized.get("category"),
            normalized.get("file_path"),
            normalized.get("line_start"),
            normalized.get("line_end"),
            normalized.get("message"),
        )

        if key not in seen:
            seen.add(key)
            unique.append(normalized)

    return ReviewResult(
        summary=f"Found {len(unique)} issue(s).",
        findings=unique,
        model_used="local-stub",
        duration_ms=0,
    )