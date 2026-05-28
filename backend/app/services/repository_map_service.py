from collections import defaultdict

import os


repository_map = defaultdict(list)


def build_repository_map(files):

    global repository_map

    repository_map.clear()

    for file_path in files:

        filename = os.path.basename(file_path)

        repository_map[filename] = file_path

    return repository_map


def find_related_files(query: str):

    matches = []

    query = query.lower()

    for filename, path in repository_map.items():

        if query in filename.lower():

            matches.append(path)

    return matches