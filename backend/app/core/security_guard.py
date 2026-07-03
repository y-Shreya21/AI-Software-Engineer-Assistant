import re
from fastapi import HTTPException, status

# Regex rules for detecting credentials
SECRET_PATTERNS = {
    "AWS_KEY": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "OPENAI_KEY": r"sk-[a-zA-Z0-9]{20,}|sk-proj-[a-zA-Z0-9_]{30,}",
    "GITHUB_PAT": r"ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}",
    "DATABASE_URL": r"(?:postgresql\+asyncpg|postgresql|redis|mongodb):\/\/[a-zA-Z0-9_]+:[^@]+@[a-zA-Z0-9_.-]+:[0-9]+",
    "PRIVATE_KEY": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+ PRIVATE KEY-----"
}

# Key phrases associated with jailbreak or prompt injection attacks
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "system override",
    "you are now a",
    "do anything now",
    "jailbreak",
    "dan mode",
    "bypass safety",
    "forget your guidelines"
]

def redact_secrets(text: str) -> str:
    """
    Scans code snippets or text chunks and replaces sensitive credentials with redaction strings.
    """
    if not text:
        return text
        
    redacted_text = text
    for secret_type, pattern in SECRET_PATTERNS.items():
        redacted_text = re.sub(pattern, f"[REDACTED_{secret_type}]", redacted_text, flags=re.IGNORECASE)
        
    return redacted_text

def validate_prompt(prompt: str) -> str:
    """
    Validates user queries against prompt injection and instructions hijacking.
    Raises HTTPException 400 if malicious payload is detected.
    """
    if not prompt:
        return prompt
        
    normalized = prompt.lower()
    for phrase in INJECTION_KEYWORDS:
        if phrase in normalized:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security validation failed: Potential prompt injection or system override detected."
            )
            
    return prompt

def sanitize_file_path(filename: str) -> str:
    """
    Protects against path traversal attacks (e.g. ../../etc/passwd).
    """
    if not filename:
        return ""
        
    # Remove leading slashes and dot-dot occurrences
    sanitized = filename.replace("../", "").replace("..\\", "")
    sanitized = re.sub(r"[\\/]+", "/", sanitized)  # normalize slashes
    return sanitized.strip("/")
