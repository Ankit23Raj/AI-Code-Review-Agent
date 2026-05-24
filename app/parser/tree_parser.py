import ast

from app.reviewer.schemas import CodeFact


def parse_file(file_path, content, changed_lines):
    tree = ast.parse(content)
    lines = content.splitlines()
    facts = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = getattr(node, "end_lineno", start_line)
            snippet_lines = lines[start_line - 1 : end_line]
            snippet = "\n".join(snippet_lines)

            facts.append(
                CodeFact(
                    file_path=file_path,
                    language="python",
                    symbol_name=node.name,
                    start_line=start_line,
                    end_line=end_line,
                    snippet=snippet,
                )
            )

    return facts
