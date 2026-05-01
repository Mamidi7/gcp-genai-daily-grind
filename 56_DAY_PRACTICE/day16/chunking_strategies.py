"""Day 16: 3 chunking strategies + cosine similarity baseline.

Requires: numpy>=1.26.0, pydantic>=2.7.1
Extends: day15_rag/llm_api_wrapper.py (uses same pydantic/validation rigor)
"""

from __future__ import annotations

import json
import logging
import math
import re
from typing import Callable

import numpy as np
from pydantic import BaseModel, Field, field_validator

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}',
)
logger = logging.getLogger(__name__)


class TextChunk(BaseModel):
    """Validated chunk ready for embedding or retrieval."""

    text: str = Field(..., min_length=1)
    strategy: str = Field(..., pattern=r"^(fixed|recursive|semantic)$")
    index: int = Field(..., ge=0)
    char_start: int = Field(..., ge=0)
    char_end: int = Field(..., ge=0)
    token_estimate: int = Field(..., ge=1)

    @field_validator("char_end")
    @classmethod
    def end_after_start(cls, v: int, info) -> int:
        if "char_start" in info.data and v < info.data["char_start"]:
            raise ValueError("char_end must be >= char_start")
        return v

    def to_log_fields(self) -> dict:
        return {
            "strategy": self.strategy,
            "index": self.index,
            "token_estimate": self.token_estimate,
            "length": self.char_end - self.char_start,
        }


def _token_estimate(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English."""
    return max(1, math.ceil(len(text) / 4))


def chunk_fixed(text: str, chunk_size: int = 200, overlap: int = 50) -> list[TextChunk]:
    """Fixed-size sliding window. Fast. Risk: cuts mid-sentence."""
    chunks: list[TextChunk] = []
    step = chunk_size - overlap
    idx = 0
    pos = 0
    while pos < len(text):
        end = min(pos + chunk_size, len(text))
        snippet = text[pos:end]
        chunks.append(
            TextChunk(
                text=snippet,
                strategy="fixed",
                index=idx,
                char_start=pos,
                char_end=end,
                token_estimate=_token_estimate(snippet),
            )
        )
        pos += step
        idx += 1
    logger.info(json.dumps({"event": "chunk_fixed", "count": len(chunks), "input_chars": len(text)}))
    return chunks


def chunk_recursive(text: str, max_chars: int = 300) -> list[TextChunk]:
    """Sentence-aware recursive split. Preserves boundaries. Slower."""
    chunks: list[TextChunk] = []
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    current: list[str] = []
    current_len = 0
    idx = 0

    for sent in sentences:
        sent_len = len(sent)
        if current_len + sent_len + 1 > max_chars and current:
            snippet = " ".join(current)
            start = text.find(snippet)
            end = start + len(snippet) if start != -1 else -1
            chunks.append(
                TextChunk(
                    text=snippet,
                    strategy="recursive",
                    index=idx,
                    char_start=max(0, start),
                    char_end=max(0, end),
                    token_estimate=_token_estimate(snippet),
                )
            )
            idx += 1
            current = [sent]
            current_len = sent_len
        else:
            current.append(sent)
            current_len += sent_len + 1

    if current:
        snippet = " ".join(current)
        start = text.find(snippet)
        end = start + len(snippet) if start != -1 else -1
        chunks.append(
            TextChunk(
                text=snippet,
                strategy="recursive",
                index=idx,
                char_start=max(0, start),
                char_end=max(0, end),
                token_estimate=_token_estimate(snippet),
            )
        )
    logger.info(json.dumps({"event": "chunk_recursive", "count": len(chunks), "input_chars": len(text)}))
    return chunks


def chunk_semantic(text: str, max_chars: int = 400) -> list[TextChunk]:
    """Paragraph-aware split. Best for docs with clear sections."""
    chunks: list[TextChunk] = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    idx = 0
    char_cursor = 0

    for para in paragraphs:
        if len(para) > max_chars:
            # fallback to recursive for oversized paragraphs
            sub = chunk_recursive(para, max_chars=max_chars)
            for s in sub:
                s.strategy = "semantic"
                s.index = idx
                idx += 1
                chunks.append(s)
            char_cursor += len(para) + 2
            continue

        start = text.find(para, char_cursor)
        end = start + len(para)
        chunks.append(
            TextChunk(
                text=para,
                strategy="semantic",
                index=idx,
                char_start=start,
                char_end=end,
                token_estimate=_token_estimate(para),
            )
        )
        char_cursor = end + 2
        idx += 1
    logger.info(json.dumps({"event": "chunk_semantic", "count": len(chunks), "input_chars": len(text)}))
    return chunks


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D vectors. Range [-1, 1]."""
    if a.shape != b.shape:
        raise ValueError(f"Shape mismatch: {a.shape} vs {b.shape}")
    dot = float(np.dot(a, b))
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed_fake(text: str, dim: int = 768) -> np.ndarray:
    """Deterministic fake embedding for local testing (no API cost)."""
    # deterministic hash-based embedding so tests are stable
    h = hash(text) % (2**31)
    rng = np.random.default_rng(seed=h)
    vec = rng.standard_normal(dim).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec


def retrieve_top_k(
    query: str,
    chunks: list[TextChunk],
    embed_fn: Callable[[str], np.ndarray] = embed_fake,
    k: int = 3,
    threshold: float = 0.0,
) -> list[tuple[float, TextChunk]]:
    """Return top-k chunks by cosine similarity to query embedding."""
    q_vec = embed_fn(query)
    scored: list[tuple[float, TextChunk]] = []
    for ch in chunks:
        c_vec = embed_fn(ch.text)
        sim = cosine_similarity(q_vec, c_vec)
        scored.append((sim, ch))
    scored.sort(key=lambda x: x[0], reverse=True)
    filtered = [(s, c) for s, c in scored if s >= threshold]
    result = filtered[:k]
    logger.info(
        json.dumps(
            {
                "event": "retrieve_top_k",
                "k_requested": k,
                "k_returned": len(result),
                "best_score": round(float(scored[0][0]), 4) if scored else None,
                "threshold": threshold,
            }
        )
    )
    return result


# ------------------------------------------------------------------
# Demo / smoke test
# ------------------------------------------------------------------

SAMPLE_DOC = """Google Cloud Platform (GCP) offers a wide range of AI and ML services.

Vertex AI is the unified platform for building, deploying, and scaling ML models.
It supports both custom training and AutoML. You can deploy models to endpoints
for online prediction or run batch jobs for large datasets.

BigQuery ML lets you create and execute machine learning models in BigQuery
using standard SQL. This reduces data movement because your data already lives
in BigQuery.

For generative AI, GCP provides the Gemini family of models through Vertex AI.
These models support multimodal inputs including text, images, and video.
Application developers can use the Gemini API to build chatbots, summarizers,
and code assistants.

Retrieval Augmented Generation (RAG) is a common pattern on GCP. You store
embeddings in BigQuery using VECTOR_SEARCH and retrieve relevant chunks
before sending them to Gemini for grounded generation."""


def _smoke() -> None:
    print("=== FIXED SIZE ===")
    fixed = chunk_fixed(SAMPLE_DOC, chunk_size=180, overlap=30)
    for c in fixed[:3]:
        print(f"[{c.index}] tokens={c.token_estimate} | {c.text[:60]}...")

    print("\n=== RECURSIVE ===")
    rec = chunk_recursive(SAMPLE_DOC, max_chars=250)
    for c in rec[:3]:
        print(f"[{c.index}] tokens={c.token_estimate} | {c.text[:60]}...")

    print("\n=== SEMANTIC ===")
    sem = chunk_semantic(SAMPLE_DOC, max_chars=300)
    for c in sem[:3]:
        print(f"[{c.index}] tokens={c.token_estimate} | {c.text[:60]}...")

    print("\n=== RETRIEVAL ===")
    query = "How does BigQuery ML work?"
    for name, chunks in [("fixed", fixed), ("recursive", rec), ("semantic", sem)]:
        hits = retrieve_top_k(query, chunks, k=2)
        print(f"\n{name}:")
        for score, hit in hits:
            print(f"  score={score:.4f} [{hit.index}] {hit.text[:70]}...")


if __name__ == "__main__":
    _smoke()
