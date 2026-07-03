import ollama

from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_similar_code
from app.services.repository_map_service import (
    find_related_files
)


def _build_prompt(question: str) -> tuple[str, list]:

    from app.core.security_guard import validate_prompt
    validate_prompt(question)

    query_embedding = generate_embedding(
        question
    )

    related_files = find_related_files(
        question
    )

    results = search_similar_code(
        query_embedding,
        limit=5,
    )

    related_context = ""

    for file_path in related_files[:5]:

        try:

            with open(file_path, "r") as file:

                related_context += (
                    f"\n\nFILE: {file_path}\n"
                )

                related_context += file.read()

        except Exception:

            continue

    vector_context = "\n\n".join([
        result.payload.get("content", "")
        for result in results
    ])

    context = (
        vector_context
        + "\n\n"
        + related_context
    )

    prompt = f"""
You are an AI Software Engineer Assistant.

Answer the user's question using ONLY
the provided repository context.

Repository Context:
{context}

Question:
{question}
"""

    sources = [
        result.payload.get("file_path")
        for result in results
    ]

    return prompt, sources

def ask_repository(question: str):
    prompt, sources = _build_prompt(question)

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return {
        "answer": response["message"]["content"],
        "sources": sources,
    }


def stream_repository_answer(question: str):
    prompt, _sources = _build_prompt(question)

    stream = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=True,
    )

    for chunk in stream:
        content = chunk["message"]["content"]
        if content:
            yield content
