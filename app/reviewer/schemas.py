from dataclasses import dataclass
from typing import List


@dataclass
class CodeFact:
    file_path: str
    language: str
    symbol_name: str
    start_line: int
    end_line: int
    snippet: str = ""


@dataclass
class Finding:
    severity: str
    category: str
    file_path: str
    line_start: int
    line_end: int
    message: str
    suggestion: str
    confidence: float
    agent_name: str


@dataclass
class ReviewResult:
    summary: str
    findings: List[Finding]
    model_used: str = ""
    duration_ms: int = 0