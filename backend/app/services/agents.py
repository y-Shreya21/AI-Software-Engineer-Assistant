import ollama
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_similar_code
from app.services.repository_map_service import find_related_files

class RetrievalAgent:
    def retrieve_context(self, query: str, limit: int = 5) -> dict:
        """
        Retrieves codebase snippets using Qdrant vector similarity and structural repository maps.
        """
        print("[RetrievalAgent] Executing vector similarity search...")
        embedding = generate_embedding(query)
        results = search_similar_code(embedding, limit=limit)
        
        print("[RetrievalAgent] Locating related files via structural relation mapping...")
        related_files = find_related_files(query)
        
        # Format retrieval context
        vector_context = "\n\n".join([
            f"FILE: {r.payload.get('file_path')}\n{r.payload.get('content', '')}" 
            for r in results
        ])
        
        related_context = ""
        for path in related_files[:3]:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    related_context += f"\n\nFILE: {path}\n" + f.read()
            except Exception:
                continue
                
        return {
            "context": vector_context + "\n\n" + related_context,
            "sources": list(set([r.payload.get("file_path") for r in results]))
        }

class AnalysisAgent:
    def explain_code(self, code: str) -> str:
        """
        Generates functional explanation, dependencies, and risks for code.
        """
        print("[AnalysisAgent] Explaining code snippet...")
        prompt = f"""
You are an expert senior software architect.
Explain this code detailing:
1. Purpose and functionality
2. Main responsibilities
3. Dependencies
4. Potential risks and architectural concerns

Code:
{code}
"""
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

class TestAgent:
    def generate_tests(self, code: str) -> str:
        """
        Generates pytest unit tests covering edge cases.
        """
        print("[TestAgent] Generating pytest test cases...")
        prompt = f"""
You are an expert python testing engineer.
Generate comprehensive pytest unit tests for the following code:
- Check edge cases
- Use mock values/functions if external dependencies exist
- Use standard pytest format

Code:
{code}
"""
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

class BugAgent:
    def suggest_fixes(self, code: str) -> str:
        """
        Runs static review to identify bugs and outputs improved code.
        """
        print("[BugAgent] Analyzing code for bugs and security vulnerabilities...")
        prompt = f"""
You are an expert senior software engineer.
Analyze the following code for:
- Logic bugs and errors
- Code quality issues or bad practices
- Performance concerns

Return the improved code and detailed explanations of the changes.

Code:
{code}
"""
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

class CoordinatorAgent:
    def route_request(self, query: str, code: str = None) -> dict:
        """
        Routes incoming requests to the target sub-agents based on context and query intent.
        """
        query_lower = query.lower()
        print(f"[CoordinatorAgent] Processing incoming command: '{query}'")
        
        if "test" in query_lower:
            print("[CoordinatorAgent] Intent matches 'test generation'. Delegating to TestAgent.")
            tests = TestAgent().generate_tests(code or query)
            return {
                "type": "tests",
                "answer": tests,
                "sources": []
            }
            
        elif "bug" in query_lower or "fix" in query_lower:
            print("[CoordinatorAgent] Intent matches 'bug analysis'. Delegating to BugAgent.")
            fixes = BugAgent().suggest_fixes(code or query)
            return {
                "type": "fix",
                "answer": fixes,
                "sources": []
            }
            
        elif "explain" in query_lower or "analyze" in query_lower:
            print("[CoordinatorAgent] Intent matches 'code explanation'. Delegating to AnalysisAgent.")
            explanation = AnalysisAgent().explain_code(code or query)
            return {
                "type": "review",
                "answer": explanation,
                "sources": []
            }
            
        else:
            print("[CoordinatorAgent] Intent matches 'codebase chat'. Delegating to RetrievalAgent.")
            context_data = RetrievalAgent().retrieve_context(query)
            
            prompt = f"""
You are an AI Software Engineer Assistant.
Answer the user's question using ONLY the provided repository context.

Repository Context:
{context_data['context']}

Question:
{query}
"""
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            return {
                "type": "chat",
                "answer": response["message"]["content"],
                "sources": context_data["sources"]
            }
