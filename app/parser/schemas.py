from dataclasses import dataclass
from typing import List

@dataclass
class CodeFact:
    file_path: str
    symbol_name: str
    start_line: int
    end_line: int
    imports: List[str]
    literals: List[str]
    snippet: str