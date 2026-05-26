from tree_sitter import Language, Parser
import tree_sitter_python as tspython
from app.parser.schemas import CodeFact

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)


def get_imports(root, code):
    imports = []

    def walk(node):
        if node.type in ("import_statement", "import_from_statement"):
            text = code[node.start_byte:node.end_byte].decode()
            imports.append(text)
        for child in node.children:
            walk(child)

    walk(root)
    return imports


def get_literals(node, code):
    literals = []

    def walk(n):
        if n.type == "string":
            text = code[n.start_byte:n.end_byte].decode()
            literals.append(text)
        for child in n.children:
            walk(child)

    walk(node)
    return literals


def parse_file(file_path: str, content: str, changed_lines=None):
    code = content.encode("utf8")
    tree = parser.parse(code)
    root = tree.root_node
    facts = []

    imports = get_imports(root, code)
    changed_set = set(changed_lines) if changed_lines else None

    def overlaps(start_line: int, end_line: int) -> bool:
        if not changed_set:
            return True
        return any(line in changed_set for line in range(start_line, end_line + 1))

    def walk(node):
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1

                if overlaps(start_line, end_line):
                    symbol_name = code[name_node.start_byte:name_node.end_byte].decode()
                    snippet = code[node.start_byte:node.end_byte].decode()
                    literals = get_literals(node, code)

                    facts.append(
                        CodeFact(
                            file_path=file_path,
                            symbol_name=symbol_name,
                            start_line=start_line,
                            end_line=end_line,
                            imports=imports,
                            literals=literals,
                            snippet=snippet,
                        )
                    )

        for child in node.children:
            walk(child)

    walk(root)
    return facts


if __name__ == "__main__":
    sample = """
import sqlite3

def login():
    query = "SELECT * FROM users"
    print(query)
"""
    result = parse_file("sample.py", sample, changed_lines=[4, 5])
    for fact in result:
        print(fact)