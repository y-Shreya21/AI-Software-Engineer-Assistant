import ollama

from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_similar_code


def ask_repository(question: str):

    query_embedding = generate_embedding(
        question
    )

    results = search_similar_code(
        query_embedding,
        limit=5
    )

    context = "\n\n".join([
        result.payload.get("content", "")
        for result in results
    ])

    prompt = f"""
You are an AI Software Engineer Assistant.

Answer the user's question using ONLY
the provided repository context.

Repository Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="phi3",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": [
            result.payload.get("file_path")
            for result in results
        ]
    }