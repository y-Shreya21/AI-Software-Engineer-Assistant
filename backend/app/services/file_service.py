import os

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx"
}

IGNORED_DIRECTORIES = {
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "coverage"
}

def scan_repository(repo_path: str):
    scanned_files = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORED_DIRECTORIES
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext in SUPPORTED_EXTENSIONS:

                full_path = os.path.join(root, file)

                scanned_files.append(full_path)

    return scanned_files