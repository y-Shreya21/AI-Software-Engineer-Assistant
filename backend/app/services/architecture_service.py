import ast
import os
from collections import defaultdict


def analyze_dependencies(files):

    graph = defaultdict(list)

    for file_path in files:

        if not file_path.endswith(".py"):
            continue

        filename = os.path.basename(file_path)

        try:

            with open(file_path, "r") as file:

                content = file.read()

            tree = ast.parse(content)

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.ImportFrom):

                    if node.module:

                        if node.module.startswith("app"):

                            imports.append(
                                node.module
                            )

            graph[filename] = imports

        except Exception:

            continue

    return dict(graph)
def clean(name):

    return (
        name.replace(".py", "")
        .replace(".", "_")
        .replace("/", "_")
    )


def generate_mermaid(graph):

    lines = ["graph LR"]

    added = set()

    for source, targets in graph.items():

        source_name = clean(source)

        for target in targets:

            target_name = clean(
                target.replace("app.", "")
            )

            edge = (
                f"{source_name} --> {target_name}"
            )

            if edge not in added:

                added.add(edge)

                lines.append(edge)

    return "\n".join(lines)