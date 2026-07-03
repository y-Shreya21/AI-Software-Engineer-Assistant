import os
from app.services.code_parser import parse_code

repository_map = {}

def build_repository_map(files):
    """
    Parses and indexes structural symbols and dependency maps for all scanned files.
    """
    global repository_map
    repository_map.clear()
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            metadata = parse_code(file_path, content)
        except Exception:
            metadata = {
                "language": "unknown",
                "classes": [],
                "functions": [],
                "dependencies": [],
                "docstrings": "",
                "symbols": []
            }
            
        repository_map[file_path] = {
            "filename": filename,
            "metadata": metadata
        }
        
    return repository_map

def find_related_files(query: str):
    """
    Language-aware matching searching filenames, classes, functions, and imports.
    """
    matches = []
    query = query.lower()
    
    for path, data in repository_map.items():
        filename = data["filename"]
        metadata = data["metadata"]
        
        # 1. Filename match
        if query in filename.lower():
            matches.append(path)
            continue
            
        # 2. Class names match
        if any(query in c.lower() for c in metadata["classes"]):
            matches.append(path)
            continue
            
        # 3. Function names match
        if any(query in f.lower() for f in metadata["functions"]):
            matches.append(path)
            continue
            
        # 4. Imports/Dependencies match
        if any(query in d.lower() for d in metadata["dependencies"]):
            matches.append(path)
            continue
            
    return matches