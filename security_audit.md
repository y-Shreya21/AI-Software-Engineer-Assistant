# Security Audit & Hardening Report

This report documents the security mechanisms, vulnerability mitigation controls, and verification testing completed for the **AI Software Engineer Assistant** project.

---

## 1. Vulnerability Assessment & Mitigation Matrix

| Vulnerability Category | Risk Description | Implemented Countermeasure | Verification Status |
|:---|:---|:---|:---|
| **SQL Injection** | Malicious input manipulating SQL queries. | Applied **SQLAlchemy ORM** parameterized async queries exclusively via Pydantic model validations. | **Verified** |
| **Credential & Secret Exposure** | Embedding AWS, OpenAI, or database keys into vector databases or exposing them to LLMs. | Built a **Secret Scanner & Redactor** (`security_guard.py`) filtering file chunks before tokenization. | **Verified** (test_security.py) |
| **Prompt Injection / Jailbreaking** | Instructing the model to ignore guidelines and leak workspace context. | Built a **Prompt Shield** (`security_guard.py`) validating queries against instructions override attempts. | **Verified** (test_security.py) |
| **Path Traversal / Local File Inclusion** | Constructing `../../etc/passwd` file paths in ingestion or viewing. | Implemented a **Path Sanitizer** cleaning relative trajectories and dot-dot strings. | **Verified** (test_security.py) |
| **DoS & Exhaustion Attacks** | Brute forcing auth routes or sending massive indexing requests. | Configured an asynchronous **Redis Rate Limiter** mapping client IPs to token windows. | **Verified** |
| **XSS & Clickjacking** | Injecting scripts or framing the application. | Integrated security headers middleware (`X-Frame-Options: DENY`, `Content-Security-Policy`). | **Verified** |

---

## 2. Hardening Configurations Details

### **A. Token-Based Hashing (Python 3.13 Ready)**
* **Problem**: Standard `passlib` bcrypt mixins crash on Python 3.13 due to wrap-bug checking incompatibilities with `bcrypt` v4+.
* **Solution**: Developed a direct cryptography binding in `auth_utils.py` using `bcrypt` natively:
  ```python
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
  ```

### **B. Security Guards (`app/core/security_guard.py`)**
* Scans chunks before embedding using pre-compiled regex signatures for AWS Keys, OpenAI Project/User Keys, GitHub PATs, and Database URIs.
* Replaces matched targets with standard `[REDACTED_SECRET]` tags.

---

## 3. Automated Test Logs
All tests ran and passed:
```text
tests/test_auth.py ...                                                   [ 33%]
tests/test_parser.py ...                                                 [ 66%]
tests/test_security.py ...                                               [100%]
======================== 9 passed in 1.33s =========================
```
