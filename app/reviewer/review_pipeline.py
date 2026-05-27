import logging
from typing import Any, Dict, List

from app.github.github_client import get_changed_files
from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown
from app.parser.tree_parser import parse_file
from app.agents.security import run_security_agent
from app.agents.logic import run_logic_agent
from app.agents.style import run_style_agent


logger = logging.getLogger(__name__)


def _log(level: int, message: str) -> None:
    logger.log(level, message)
    try:
        from app.utils.logger import log as app_log

        app_log(message, level="ERROR" if level >= logging.ERROR else "INFO")
    except Exception:
        pass


def _validate_payload(payload: dict) -> Dict[str, Any]:
    _log(logging.INFO, "Payload validation started")

    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")

    repo_path = payload.get("repo_path") or payload.get("repository", {}).get("full_name")
    pr_number = payload.get("pr_number") or payload.get("pull_request", {}).get("number")
    changed_files = payload.get("changed_files")

    if not repo_path:
        raise ValueError("Missing repo_path")

    if pr_number is None:
        raise ValueError("Missing pr_number")

    if changed_files is None:
        changed_files = get_changed_files(repo_path, pr_number)

    if not isinstance(changed_files, list):
        raise ValueError("changed_files must be a list")

    return {
        "repo_path": repo_path,
        "pr_number": pr_number,
        "changed_files": changed_files,
    }


def _review_file(file_entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    file_path = file_entry.get("file_path")
    content = file_entry.get("content")
    changed_lines = file_entry.get("changed_lines", [])

    if not file_path or not content:
        _log(logging.ERROR, "Failed processing file")
        return []

    _log(logging.INFO, "Processing file")

    try:
        parse_file(file_path, content, changed_lines)

        _log(logging.INFO, "Running agents")

        findings: List[Dict[str, Any]] = []

        findings.extend(run_security_agent(content))
        findings.extend(run_logic_agent(content))
        findings.extend(run_style_agent(content))

        return findings
    except Exception as error:
        _log(logging.ERROR, f"Failed processing file: {error}")
        return []


def review_payload(payload: dict):
    try:
        validated_payload = _validate_payload(payload)

        collected_findings: List[Dict[str, Any]] = []
        for file_entry in validated_payload["changed_files"]:
            collected_findings.extend(_review_file(file_entry))

        _log(logging.INFO, "Aggregating findings")
        aggregated_findings = aggregate_findings(collected_findings)

        _log(logging.INFO, "Generating markdown review")
        markdown = format_review_markdown(aggregated_findings)

        _log(logging.INFO, "Review completed")

        return {
            "summary": getattr(aggregated_findings, "summary", "AI Review Summary"),
            "repo_path": validated_payload["repo_path"],
            "pr_number": validated_payload["pr_number"],
            "files_reviewed": len(validated_payload["changed_files"]),
            "findings": getattr(aggregated_findings, "findings", []),
            "model_used": getattr(aggregated_findings, "model_used", ""),
            "duration_ms": getattr(aggregated_findings, "duration_ms", 0),
            "markdown": markdown,
        }
    except Exception as error:
        _log(logging.ERROR, f"Failed processing file: {error}")
        raise