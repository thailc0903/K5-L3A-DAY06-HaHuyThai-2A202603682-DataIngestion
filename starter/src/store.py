"""Persistent Qdrant local collections, cosine search, trusted-field filtering."""
import math
import uuid
from typing import Any
from .models import Chunk


class QdrantStore:
    ALLOWED_FILTERS = {"category", "version", "language", "document_type", "module"}

    def __init__(self, path: str, dimensions: int) -> None:
        from qdrant_client import QdrantClient
        if dimensions < 1:
            raise ValueError("Invalid vector dimensions")
        self.client = QdrantClient(path=path)
        self.dimensions = dimensions

    def create_schema(self) -> None:
        from qdrant_client import models
        for strategy in ("A", "B", "C"):
            name = self.collection(strategy)
            if not self.client.collection_exists(name):
                self.client.create_collection(name, vectors_config=models.VectorParams(
                    size=self.dimensions, distance=models.Distance.COSINE))
            else:
                config = self.client.get_collection(name).config.params.vectors
                if config.size != self.dimensions or config.distance != models.Distance.COSINE:
                    raise ValueError("Existing collection uses incompatible vector settings")

    @staticmethod
    def collection(strategy):
        if strategy not in {"A", "B", "C"}:
            raise ValueError("Unknown strategy")
        return "python313_" + strategy

    def validate_vector(self, vector):
        if len(vector) != self.dimensions or not all(math.isfinite(v) for v in vector):
            raise ValueError("Vector dimension mismatch or nonfinite values")

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        from qdrant_client import models
        if len(chunks) != len(vectors):
            raise ValueError("Chunk/vector count mismatch")
        points = []
        for chunk, vector in zip(chunks, vectors):
            self.validate_vector(vector)
            payload = {**chunk.metadata, "chunk_id": chunk.chunk_id, "document_id": chunk.document_id,
                       "source": chunk.source, "page": chunk.page, "text": chunk.text}
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, chunk.chunk_id))
            points.append(models.PointStruct(id=point_id, vector=vector, payload=payload))
        name = self.collection(strategy)
        # A complete corpus synchronization: remove stale/deleted source chunks.
        old, offset = set(), None
        while True:
            records, offset = self.client.scroll(name, limit=256, offset=offset, with_payload=False, with_vectors=False)
            old.update(str(p.id) for p in records)
            if offset is None:
                break
        for start in range(0, len(points), 128):
            self.client.upsert(name, points=points[start:start + 128], wait=True)
        obsolete = sorted(old - {str(p.id) for p in points})
        if obsolete:
            self.client.delete(name, points_selector=models.PointIdsList(points=obsolete), wait=True)

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        from qdrant_client import models
        self.validate_vector(query_vector)
        if top_k < 1:
            raise ValueError("top_k must be positive")
        conditions = []
        for key, value in (filters or {}).items():
            if key not in self.ALLOWED_FILTERS or not isinstance(value, (str, int, bool)):
                raise ValueError(f"Unsupported filter: {key}")
            conditions.append(models.FieldCondition(key=key, match=models.MatchValue(value=value)))
        found = self.client.query_points(self.collection(strategy), query=query_vector, limit=top_k,
            query_filter=models.Filter(must=conditions) if conditions else None, with_payload=True).points
        results = []
        for point in found:
            payload = dict(point.payload)
            text = payload.pop("text")
            chunk_id = payload.pop("chunk_id")
            results.append({"chunk_id": chunk_id, "text": text, "score": float(point.score), "metadata": payload})
        return results

    def count(self, strategy):
        return self.client.count(self.collection(strategy), exact=True).count

    def close(self):
        self.client.close()
