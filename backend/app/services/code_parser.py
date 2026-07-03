import ast
import os
import re

def parse_code(file_path: str, content: str) -> dict:
    """
    Parses structural metadata (classes, functions, imports, docstrings)
    across Python, JavaScript/TypeScript, Java, Go, and C++.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    result = {
        "language": _detect_language(ext),
        "classes": [],
        "functions": [],
        "dependencies": [],
        "docstrings": "",
        "symbols": []
    }
    
    if ext == ".py":
        _parse_python(content, result)
    elif ext in [".js", ".jsx", ".ts", ".tsx"]:
        _parse_js_ts(content, result)
    elif ext == ".java":
        _parse_java(content, result)
    elif ext == ".go":
        _parse_go(content, result)
    elif ext in [".cpp", ".hpp", ".h", ".cc"]:
        _parse_cpp(content, result)
        
    return result

def _detect_language(ext: str) -> str:
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".h": "cpp",
        ".hpp": "cpp"
    }
    return mapping.get(ext, "unknown")

def _parse_python(content: str, result: dict):
    try:
        tree = ast.parse(content)
        # Extract docstring
        doc = ast.get_docstring(tree)
        if doc:
            result["docstrings"] = doc
            
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)
                result["symbols"].append({"name": node.name, "type": "class", "line": node.lineno})
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                result["functions"].append(node.name)
                result["symbols"].append({"name": node.name, "type": "function", "line": node.lineno})
            elif isinstance(node, ast.Import):
                for name in node.names:
                    result["dependencies"].append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    result["dependencies"].append(node.module)
    except Exception:
        # Fallback to regex if parsing fails due to syntax errors
        pass

def _parse_js_ts(content: str, result: dict):
    # Match imports: import { x } from 'y' or const x = require('y')
    import_matches = re.findall(r"(?:import|from)\s+['\"]([^'\"]+)['\"]", content)
    require_matches = re.findall(r"require\(['\"]([^'\"]+)['\"]\)", content)
    result["dependencies"] = list(set(import_matches + require_matches))
    
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        # Match classes
        class_match = re.search(r"class\s+([a-zA-Z0-9_$]+)", line)
        if class_match:
            name = class_match.group(1)
            result["classes"].append(name)
            result["symbols"].append({"name": name, "type": "class", "line": idx})
            
        # Match functions
        func_match = re.search(r"(?:function\s+([a-zA-Z0-9_$]+)|const\s+([a-zA-Z0-9_$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", line)
        if func_match:
            name = func_match.group(1) or func_match.group(2)
            if name:
                result["functions"].append(name)
                result["symbols"].append({"name": name, "type": "function", "line": idx})

def _parse_java(content: str, result: dict):
    # Match imports: import x.y.z;
    result["dependencies"] = re.findall(r"import\s+([a-zA-Z0-9_.]+);", content)
    
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        # Match classes
        class_match = re.search(r"class\s+([a-zA-Z0-9_$]+)", line)
        if class_match:
            name = class_match.group(1)
            result["classes"].append(name)
            result["symbols"].append({"name": name, "type": "class", "line": idx})
            
        # Match methods (simple public/private/protected pattern)
        method_match = re.search(r"(?:public|private|protected)\s+(?:async\s+)?[\w<>]+\s+([a-zA-Z0-9_]+)\s*\(", line)
        if method_match:
            name = method_match.group(1)
            result["functions"].append(name)
            result["symbols"].append({"name": name, "type": "method", "line": idx})

def _parse_go(content: str, result: dict):
    # Match imports
    imports = re.findall(r"import\s+\((.*?)\)", content, re.DOTALL)
    for block in imports:
        result["dependencies"].extend(re.findall(r'"([^"]+)"', block))
    single_imports = re.findall(r'import\s+"([^"]+)"', content)
    result["dependencies"].extend(single_imports)
    
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        # Match Go functions/methods: func functionName or func (x *Type) methodName
        func_match = re.search(r"func\s+(?:\([^)]*\)\s*)?([a-zA-Z0-9_]+)\s*\(", line)
        if func_match:
            name = func_match.group(1)
            result["functions"].append(name)
            result["symbols"].append({"name": name, "type": "function", "line": idx})

def _parse_cpp(content: str, result: dict):
    # Match includes: #include <vector> or #include "header.h"
    includes = re.findall(r'#include\s+["<]([^">]+)[">]', content)
    result["dependencies"] = includes
    
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        # Match classes or structs
        class_match = re.search(r"(?:class|struct)\s+([a-zA-Z0-9_]+)", line)
        if class_match:
            name = class_match.group(1)
            result["classes"].append(name)
            result["symbols"].append({"name": name, "type": "class", "line": idx})
            
        # Match simple global function definitions
        func_match = re.search(r"^[\w:*&<>#]+[\s+]+([a-zA-Z0-9_]+)\s*\(", line)
        if func_match:
            name = func_match.group(1)
            if name not in ["if", "for", "while", "switch"]:
                result["functions"].append(name)
                result["symbols"].append({"name": name, "type": "function", "line": idx})
