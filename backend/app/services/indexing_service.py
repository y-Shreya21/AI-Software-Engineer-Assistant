import os

from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import store_embedding


def index_repository_files(files: list):

    total_chunks = 0

    for file_path in files:
        print(f"Indexing: {file_path}")

        try:

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            from app.core.security_guard import redact_secrets
            content = redact_secrets(content)
            chunks = chunk_text(content)

            for chunk in chunks:

                embedding = generate_embedding(chunk)

                metadata = {
                    "file_path": file_path
                }

                store_embedding(
                    content=chunk,
                    embedding=embedding,
                    metadata=metadata
                )

                total_chunks += 1

        except Exception as e:

            print(f"Failed indexing {file_path}: {e}")
            
    
    return total_chunks