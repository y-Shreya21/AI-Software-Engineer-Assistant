import ast

from collections import defaultdict


def analyze_dependencies(files):

    graph = defaultdict(list)

    for file_path in files:

        if not file_path.endswith(".py"):
            continue

        try:

            with open(file_path, "r") as file:

                content = file.read()

            tree = ast.parse(content)

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for name in node.names:

                        imports.append(name.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imports.append(node.module)

            graph[file_path] = imports

        except Exception as error:

            print(error)

            continue

    return dict(graph)
def clean_node_name(name):

    return (
        name.replace(".py", "")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
    )


def generate_mermaid(graph):

    lines = ["graph LR"]

    added = set()

    for source, targets in graph.items():

        source_name = clean_node_name(
            source.split("/")[-1]
        )

        for target in targets:
            if not (
                target.startswith("app")
                or target.startswith("backend")
            ):
                continue

            target_name = clean_node_name(
                target.split(".")[-1]
            )

            edge = f"{source_name} --> {target_name}"

            if edge not in added:
                added.add(edge)
                lines.append(edge)

    return "\n".join(lines)