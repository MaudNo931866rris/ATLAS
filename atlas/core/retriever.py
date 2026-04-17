"""Retriever module for ATLAS.

Handles similarity search and context retrieval from the vector store.
"""

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from atlas.core.embedder import Embedder, EmbeddingConfig


@dataclass
class RetrieverConfig:
    """Configuration for the Retriever."""

    top_k: int = 5
    score_threshold: float = 0.0
    embedding_config: EmbeddingConfig = field(default_factory=EmbeddingConfig)


@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector store along with its similarity score."""

    text: str
    score: float
    metadata: dict = field(default_factory=dict)


class Retriever:
    """Retrieves relevant chunks from an in-memory vector store using cosine similarity.

    In a production setup this would interface with a persistent vector database
    (e.g. Chroma, Pinecone, Weaviate).  For now we keep things simple and store
    embeddings in memory so the rest of the pipeline can be exercised end-to-end.
    """

    def __init__(self, config: Optional[RetrieverConfig] = None) -> None:
        self.config = config or RetrieverConfig()
        self.embedder = Embedder(self.config.embedding_config)

        # Internal store: list of (embedding_vector, text, metadata)
        self._store: list[tuple[np.ndarray, str, dict]] = []

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def add_chunks(self, chunks: list[str], metadata: Optional[list[dict]] = None) -> None:
        """Embed and store a list of text chunks.

        Args:
            chunks: Plain-text chunks to index.
            metadata: Optional per-chunk metadata dicts.  If omitted an empty
                      dict is stored for each chunk.
        """
        if not chunks:
            return

        if metadata is None:
            metadata = [{} for _ in chunks]

        if len(metadata) != len(chunks):
            raise ValueError("`metadata` length must match `chunks` length.")

        vectors = self.embedder.embed(chunks)  # shape: (n, dim)
        for vec, text, meta in zip(vectors, chunks, metadata):
            self._store.append((np.array(vec, dtype=np.float32), text, meta))

    def clear(self) -> None:
        """Remove all indexed chunks."""
        self._store.clear()

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        """Return the top-k most relevant chunks for *query*.

        Args:
            query: The user query string.

        Returns:
            A list of :class:`RetrievedChunk` objects sorted by descending
            similarity score, filtered by ``score_threshold``.
        """
        if not self._store:
            return []

        query_vec = np.array(self.embedder.embed([query])[0], dtype=np.float32)

        scores = []
        for vec, text, meta in self._store:
            score = float(_cosine_similarity(query_vec, vec))
            if score >= self.config.score_threshold:
                scores.append(RetrievedChunk(text=text, score=score, metadata=meta))

        scores.sort(key=lambda c: c.score, reverse=True)
        return scores[: self.config.top_k]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two 1-D vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))
