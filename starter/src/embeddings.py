"""Real ONNX embeddings through FastEmbed; failures propagate, never mocked."""
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """CPU embedding adapter with documented query/passage preprocessing."""

    def __init__(self, model_name: str, cache_dir: str | None = None) -> None:
        from fastembed import TextEmbedding
        self.model_name = model_name
        self.model = TextEmbedding(model_name=model_name, cache_dir=cache_dir, threads=4)
        self.dimensions = next(m["dim"] for m in TextEmbedding.list_supported_models() if m["model"] == model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self.model.passage_embed(texts, batch_size=32)]

    def embed_query(self, question: str) -> list[float]:
        return next(self.model.query_embed(question)).tolist()
