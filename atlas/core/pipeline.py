"""End-to-end RAG pipeline combining chunking, embedding, and retrieval."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from atlas.core.chunker import process_chunk
from atlas.core.embedder import Embedder, EmbeddingConfig
from atlas.core.retriever import Retriever, RetrieverConfig, RetrievedChunk


@dataclass
class PipelineConfig:
    """Configuration for the ATLAS pipeline."""

    chunk_size: int = 512
    chunk_overlap: int = 64
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    retriever: RetrieverConfig = field(default_factory=RetrieverConfig)
    top_k: int = 5


class Pipeline:
    """Orchestrates document ingestion and query retrieval.

    Example usage::

        pipeline = Pipeline()
        pipeline.ingest_text("Some long document text...")
        results = pipeline.query("What is this about?")
    """

    def __init__(self, config: Optional[PipelineConfig] = None) -> None:
        self.config = config or PipelineConfig()
        self.embedder = Embedder(self.config.embedding)
        self.retriever = Retriever(self.config.retriever)

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def ingest_text(self, text: str, source: str = "<inline>") -> int:
        """Chunk, embed, and index a raw text string.

        Args:
            text: The document text to ingest.
            source: An optional label identifying the source document.

        Returns:
            The number of chunks indexed.
        """
        chunks = process_chunk(
            text,
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap,
        )

        if not chunks:
            return 0

        embeddings = self.embedder.embed(chunks)
        self.retriever.add_chunks(chunks, embeddings, source=source)
        return len(chunks)

    def ingest_file(self, path: str | Path) -> int:
        """Read a plain-text file and ingest its contents.

        Args:
            path: Path to the text file.

        Returns:
            The number of chunks indexed.
        """
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        return self.ingest_text(text, source=str(path))

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def query(self, question: str, top_k: Optional[int] = None) -> list[RetrievedChunk]:
        """Embed a query and retrieve the most relevant chunks.

        Args:
            question: The natural-language query.
            top_k: Number of results to return (defaults to ``config.top_k``).

        Returns:
            A ranked list of :class:`~atlas.core.retriever.RetrievedChunk`.
        """
        k = top_k if top_k is not None else self.config.top_k
        query_embedding = self.embedder.embed([question])[0]
        return self.retriever.search(query_embedding, top_k=k)

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear all indexed chunks from the retriever."""
        self.retriever.clear()
