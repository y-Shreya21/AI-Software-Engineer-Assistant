from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)
import uuid

from app.core.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

COLLECTION_NAME = "codebase_vectors"


def create_collection():
    try:
        collections = client.get_collections().collections
    except Exception as error:
        print(f"Qdrant unavailable during startup: {error}")
        return

    existing = [
        collection.name
        for collection in collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_embedding(
    content: str,
    embedding: list,
    metadata: dict
):

    point = PointStruct(
        id=str(uuid.uuid4()),

        vector=embedding,

        payload={
            "content": content,
            **metadata
        }
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )
def search_similar_code(
    query_embedding: list,
    limit: int = 5
):

    results = client.query_points(
        collection_name=COLLECTION_NAME,

        query=query_embedding,

        limit=limit
    )

    return results.points
