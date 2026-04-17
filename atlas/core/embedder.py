"""Text embedding module for ATLAS.

Provides functionality to convert text chunks into vector embeddings
using configurable embedding models (OpenAI, local, etc.).
"""

from __future__ import annotations

import os
import logging
from typing import List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingConfig:
    """Configuration for the embedding model."""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        # Reduced batch size from 64 to 32 to avoid hitting rate limits on free-tier API keys
        batch_size: int = 32,
        dimensions: Optional[int] = None,
    ):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.batch_size = batch_size
        self.dimensions = dimensions


class Embedder:
    """Converts text chunks into dense vector embeddings.

    Supports OpenAI embedding models and provides batched processing
    to stay within API rate limits.

    Example:
        >>> config = EmbeddingConfig(model_name="text-embedding-3-small")
        >>> embedder = Embedder(config)
        >>> vectors = embedder.embed(["Hello world", "Another chunk"])
        >>> print(vectors.shape)  # (2, 1536)
    """

    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        self._client = None

    def _get_client(self):
        """Lazily initialise the OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI  # type: ignore
            except ImportError as exc:
                raise ImportError(
                    "openai package is required for embedding. "
                    "Install it with: pip install openai"
                ) from exc

            if not self.config.api_key:
                raise ValueError(
                    "OpenAI API key is not set. "
                    "Set OPENAI_API_KEY in your environment or pass api_key to EmbeddingConfig."
                )
            self._client = OpenAI(api_key=self.config.api_key)
        return self._client

    def embed(self, texts: List[str]) -> np.ndarray:
        """Embed a list of text strings into vectors.

        Args:
            texts: List of text strings to embed.

        Returns:
            A 2-D numpy array of shape (len(texts), embedding_dim).

        Raises:
            ValueError: If *texts* is empty.
        """
        if not texts:
            raise ValueError("Cannot embed an empty list of texts.")

        # Strip whitespace from texts before embedding to avoid wasting tokens on padding
        # Also filter out any texts that are empty after stripping to avoid API errors
        texts = [t.strip() for t in texts]
        texts = [t for t in texts if t]

        if not texts:
            raise ValueError("All texts were empty after stripping whitespace.")

        all_embeddings: List[List[float]] = []
        client = self._get_client()

        for batch_start in range(0, len(texts), self.config.batch_size):
            batch = texts[batch_start : batch_start + self.config.batch_size]
