import json
import math
import re

from app.reviewer.schemas import Finding
from app.utils.text_cleaner import clean_text


_ANSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def _remove_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text or "")


def _strip_fences(text: str) -> str:
    cleaned = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned


def _extract_json(text: str) -> str:
    if not text:
        return ""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def _normalize_severity(value) -> str:
    if not isinstance(value, str):
        return "LOW"
    severity = value.strip().upper()
    return severity if severity in {"LOW", "MEDIUM", "HIGH"} else "LOW"


def _safe_int(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _safe_float(value, default=0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(parsed) or math.isinf(parsed):
        return default
    if parsed < 0.0:
        return 0.0
    if parsed > 1.0:
        return 1.0
    return parsed


def _extract_strings(value):
    results = []
    if isinstance(value, str):
        results.append(value)
    elif isinstance(value, list):
        for item in value:
            results.extend(_extract_strings(item))
    elif isinstance(value, dict):
        for key in (
            "message",
            "issue",
            "problem",
            "error",
            "description",
            "explanation",
            "detail",
            "details",
            "summary",
            "recommendation",
            "fix",
        ):
            if key in value:
                results.extend(_extract_strings(value[key]))
    return results


def _extract_message(payload: dict) -> str:
    candidates = []
    if "message" in payload:
        candidates = _extract_strings(payload.get("message"))
    elif "issue" in payload:
        candidates = _extract_strings(payload.get("issue"))
    elif "errors" in payload:
        candidates = _extract_strings(payload.get("errors"))
    elif "findings" in payload:
        candidates = _extract_strings(payload.get("findings"))

    cleaned = [clean_text(item) for item in candidates if clean_text(item)]
    return "; ".join(cleaned)


def _extract_suggestion(payload: dict) -> str:
    for key in ("suggestion", "fix", "recommendation", "remediation"):
        if key in payload:
            candidates = _extract_strings(payload.get(key))
            cleaned = [clean_text(item) for item in candidates if clean_text(item)]
            if cleaned:
                return "; ".join(cleaned)
    return ""


def _system_fallback(agent_name: str) -> Finding:
    return Finding(
        severity="LOW",
        category="System",
        file_path="",
        line_start=0,
        line_end=0,
        message="Unable to analyze this section.",
        suggestion="Try reviewing the code again.",
        confidence=0.0,
        agent_name=agent_name,
    )


def parse_agent_response(response, category: str, agent_name: str) -> Finding:
    cleaned = _remove_ansi(str(response or "").strip())
    if not cleaned:
        return _system_fallback(agent_name)

    cleaned = cleaned.replace("\r", " ").replace("\n", " ")
    cleaned = _strip_fences(cleaned)
    candidate = _extract_json(cleaned)

    try:
        payload = json.loads(candidate, strict=False)
    except (json.JSONDecodeError, TypeError, ValueError):
        return _system_fallback(agent_name)

    if not isinstance(payload, dict):
        return _system_fallback(agent_name)

    message = _extract_message(payload)
    if not message:
        message = "Potential issue detected."

    suggestion = _extract_suggestion(payload)
    if not suggestion:
        suggestion = "Review the code and address the issue."

    file_path = payload.get("file_path") if isinstance(payload.get("file_path"), str) else ""

    return Finding(
        severity=_normalize_severity(payload.get("severity")),
        category=category,
        file_path=file_path,
        line_start=_safe_int(payload.get("line_start")),
        line_end=_safe_int(payload.get("line_end")),
        message=clean_text(message),
        suggestion=clean_text(suggestion),
        confidence=_safe_float(payload.get("confidence"), default=0.8),
        agent_name=agent_name,
    )
