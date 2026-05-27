from pathlib import Path
import ast
import javalang
import esprima


def parse_python(content):

    results=[]

    tree=ast.parse(content)

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.ClassDef
            )
        ):

            results.append({

                "symbol_name":node.name,

                "start_line":node.lineno,

                "end_line":getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "language":"python",

                "snippet":ast.unparse(node)

            })

    return results



def parse_cpp(content):

    results=[]

    lines=content.splitlines()

    for i,line in enumerate(lines):

        line=line.strip()

        if "(" in line and ")" in line and "{" in line:

            results.append({

                "symbol_name":line,

                "start_line":i+1,

                "end_line":i+1,

                "language":"cpp",

                "snippet":line

            })

    return results



def parse_java(content):

    results=[]

    tree=javalang.parse.parse(
        content
    )

    for path,node in tree:

        if isinstance(
            node,
            javalang.tree.MethodDeclaration
        ):

            results.append({

                "symbol_name":node.name,

                "start_line":
                node.position.line,

                "end_line":
                node.position.line,

                "language":"java",

                "snippet":
                node.name

            })

    return results



def parse_js(content):

    results=[]

    tree=esprima.parseScript(
        content,
        loc=True
    )

    for node in tree.body:

        if node.type=="FunctionDeclaration":

            results.append({

                "symbol_name":
                node.id.name,

                "start_line":
                node.loc.start.line,

                "end_line":
                node.loc.end.line,

                "language":
                "javascript",

                "snippet":
                content

            })

    return results




def parse_file(
    file_name,
    content,
    changed_lines
):

    ext=Path(
        file_name
    ).suffix.lower()

    try:

        if ext==".py":

            return parse_python(
                content
            )

        elif ext in [

            ".cpp",
            ".c"

        ]:

            return parse_cpp(
                content
            )

        elif ext==".java":

            return parse_java(
                content
            )

        elif ext==".js":

            return parse_js(
                content
            )

        return []

    except Exception as e:

        print(e)

        return []