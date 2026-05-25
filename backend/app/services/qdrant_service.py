from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams
)

from app.core.config import settings

client = QdrantClient(
    path="./qdrant_data"
)

COLLECTION_NAME = "codebase_vectors"


def create_collection():

    collections = client.get_collections().collections

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
from qdrant_client.models import PointStruct
import uuid


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
