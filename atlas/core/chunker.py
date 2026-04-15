"""Text chunking utilities for ATLAS document processing pipeline.

This module provides functions to split large text documents into
smaller, overlapping chunks suitable for embedding and retrieval.
"""

from typing import List, Optional


def process_chunk(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 128,
    separator: str = "\n",
) -> List[str]:
    """Split text into overlapping chunks for downstream processing.

    Args:
        text: The raw input text to be chunked.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters to overlap between consecutive chunks.
            Defaults to 128 (increased from 64) for better context preservation
            across chunk boundaries during retrieval.
        separator: Preferred split boundary character(s).

    Returns:
        A list of text chunks, each at most ``chunk_size`` characters long.

    Raises:
        ValueError: If ``chunk_overlap`` is greater than or equal to ``chunk_size``.
        ValueError: If ``chunk_size`` is not a positive integer.
    """
    if chunk_size <= 0:
        raise ValueError(
            f"chunk_size ({chunk_size}) must be a positive integer."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            f"chunk_overlap ({chunk_overlap}) must be less than chunk_size ({chunk_size})."
        )

    if not text or not text.strip():
        return []

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end >= text_length:
            # Last chunk — take whatever remains
            chunk = text[start:]
            if chunk.strip():
                chunks.append(chunk)
            break

        # Try to split on the preferred separator to avoid cutting mid-word/sentence
        split_pos = text.rfind(separator, start, end)
        if split_pos != -1 and split_pos > start:
            end = split_pos + len(separator)

        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)

        # Advance start, stepping back by overlap to preserve context
        start = end - chunk_overlap

    return chunks


def test_chunk_overlap_preserves_context(
    chunks: List[str], chunk_overlap: int
) -> bool:
    """Verify that consecutive chunks share at least ``chunk_overlap`` characters.

    This is a lightweight sanity-check helper used in tests and diagnostics.

    Args:
        chunks: The list of chunks produced by :func:`process_chunk`.
        chunk_overlap: The expected minimum overlap in characters.

    Returns:
        ``True`` if every pair of consecutive chunks satisfies the overlap
        requirement, ``False`` otherwise.
    """
    if len(chunks) < 2:
        return True  # Nothing to compare

    for i in range(len(chunks) - 1):
        current_chunk = chunks[i]
        next_chunk = chunks[i + 1]

        # Check that the tail of the current chunk appears in the next chunk
        tail = current_chunk[-chunk_overlap:]
        if tail.strip() and tail not in next_chunk:
            return False

    return True
