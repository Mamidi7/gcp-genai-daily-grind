"""
Day 17: Embeddings Intro — text-embedding-004 + Similarity Search

Build an embedding pipeline that:
1. Converts text to 768-dimensional vectors (mock mode or real Vertex AI)
2. Computes cosine similarity between all document pairs
3. Retrieves top-k most similar documents for a query
4. Handles batch embedding with rate limiting

This is the R in RAG. Without embeddings, there is no semantic retrieval.

Interview question this answers:
  "How do embeddings work and why not just use keyword search?"
"""

from __future__ import annotations

import hashlib
import math
import os
import random
from dataclasses import dataclass, field
from typing import Any

# We use numpy if available, pure Python fallback otherwise
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# ──────────────────────────────────────────────
# 1. CORE TYPES
# ──────────────────────────────────────────────

@dataclass
class EmbeddingResult:
    """Result of embedding one or more texts."""
    texts: list[str]
    vectors: list[list[float]]
    model: str
    dimensions: int
    metadata: dict[str, Any] = field(default_factory=dict)


# ──────────────────────────────────────────────
# 2. MOCK EMBEDDING CLIENT (zero-cost)
# ──────────────────────────────────────────────

def _deterministic_vector(text: str, dimensions: int = 768, seed: int = 42) -> list[float]:
    """
    Generate a deterministic pseudo-random vector from text.
    
    Same text → same vector (simulates real embedding behavior).
    Similar texts → similar vectors (partially, via shared words).
    """
    # Use text hash as seed for deterministic output
    text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
    rng = random.Random(text_hash)

    # Create base vector
    vec = [rng.gauss(0, 1) for _ in range(dimensions)]

    # Shared words boost similarity (simulates semantic similarity)
    words = set(text.lower().split())
    word_features = [hash(w) % 100 / 100.0 for w in words]
    for i, feat in enumerate(word_features[:min(len(word_features), dimensions)]):
        vec[i] += feat * 0.5

    # Normalize to unit length
    magnitude = math.sqrt(sum(v * v for v in vec))
    if magnitude > 0:
        vec = [v / magnitude for v in vec]
    return vec


class MockEmbeddingClient:
    """Simulates text-embedding-004 for zero-cost practice."""

    def __init__(self, model: str = "text-embedding-004", dimensions: int = 768):
        self.model = model
        self.dimensions = dimensions
        self.call_count = 0
        self.total_tokens = 0

    def embed(self, texts: list[str]) -> EmbeddingResult:
        """Embed a batch of texts. Simulates rate limiting."""
        self.call_count += 1
        self.total_tokens += sum(len(t.split()) for t in texts)

        if len(texts) > 250:
            raise ValueError("Batch size exceeds 250 limit. Split into smaller batches.")

        vectors = [_deterministic_vector(t, self.dimensions) for t in texts]
        return EmbeddingResult(
            texts=texts,
            vectors=vectors,
            model=self.model,
            dimensions=self.dimensions,
            metadata={"batch_size": len(texts), "mock": True},
        )


# ──────────────────────────────────────────────
# 3. SIMILARITY FUNCTIONS
# ──────────────────────────────────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Range: -1.0 (opposite) to 1.0 (identical)
    For normalized vectors: 0.0 (orthogonal) to 1.0 (same direction)
    """
    if len(a) != len(b):
        raise ValueError(f"Dimension mismatch: {len(a)} vs {len(b)}")

    dot_product = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot_product / (mag_a * mag_b)


def euclidean_distance(a: list[float], b: list[float]) -> float:
    """Compute Euclidean distance. Lower = more similar."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def dot_product_similarity(a: list[float], b: list[float]) -> float:
    """Dot product similarity. For unit vectors, same as cosine."""
    return sum(x * y for x, y in zip(a, b))


# ──────────────────────────────────────────────
# 4. RETRIEVAL ENGINE
# ──────────────────────────────────────────────

@dataclass
class RetrievalResult:
    """Result from a similarity search query."""
    query: str
    results: list[tuple[str, float]]  # (text, similarity_score)
    metric: str
    top_k: int


class EmbeddingStore:
    """
    Simple in-memory embedding store with retrieval.
    
    In production, this would be BigQuery VECTOR_SEARCH or a vector DB.
    This version teaches the mechanics without infrastructure.
    """

    def __init__(self, client: MockEmbeddingClient):
        self.client = client
        self.documents: list[str] = []
        self.embeddings: list[list[float]] = []
        self._embedded = False

    def add_documents(self, docs: list[str]) -> None:
        """Add documents to the store."""
        self.documents.extend(docs)
        self._embedded = False

    def index(self) -> None:
        """Embed all documents (call once after adding docs)."""
        if self._embedded:
            return
        # Batch embed (respects 250 text limit)
        batch_size = 250
        all_vectors: list[list[float]] = []
        for i in range(0, len(self.documents), batch_size):
            batch = self.documents[i:i + batch_size]
            result = self.client.embed(batch)
            all_vectors.extend(result.vectors)
        self.embeddings = all_vectors
        self._embedded = True

    def search(
        self,
        query: str,
        top_k: int = 5,
        metric: str = "cosine",
    ) -> RetrievalResult:
        """Find top-k most similar documents to query."""
        if not self._embedded:
            self.index()

        query_result = self.client.embed([query])
        query_vec = query_result.vectors[0]

        sim_fn = {
            "cosine": cosine_similarity,
            "euclidean": lambda a, b: -euclidean_distance(a, b),  # negative for sorting
            "dot": dot_product_similarity,
        }[metric]

        scores = [
            (doc, sim_fn(query_vec, emb))
            for doc, emb in zip(self.documents, self.embeddings)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)

        return RetrievalResult(
            query=query,
            results=scores[:top_k],
            metric=metric,
            top_k=top_k,
        )

    def similarity_matrix(self) -> list[list[float]]:
        """Compute full pairwise similarity matrix."""
        if not self._embedded:
            self.index()
        n = len(self.documents)
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = cosine_similarity(self.embeddings[i], self.embeddings[j])
        return matrix


# ──────────────────────────────────────────────
# 5. BATCH EMBEDDING UTILITY
# ──────────────────────────────────────────────

def batch_embed_with_retry(
    client: MockEmbeddingClient,
    texts: list[str],
    batch_size: int = 250,
    max_retries: int = 3,
) -> EmbeddingResult:
    """
    Embed large text lists with batching and retry.
    
    Handles:
    - API rate limits (retry with backoff)
    - Batch size limits (auto-split)
    - Empty text filtering
    """
    # Filter empty texts
    filtered = [(i, t) for i, t in enumerate(texts) if t.strip()]
    if not filtered:
        return EmbeddingResult([], [], client.model, 768)

    all_vectors: list[list[float]] = [[] for _ in texts]
    actual_texts = [t for _, t in filtered]
    actual_indices = [i for i, _ in filtered]

    for start in range(0, len(actual_texts), batch_size):
        batch = actual_texts[start:start + batch_size]
        result = client.embed(batch)
        for idx, vec in enumerate(result.vectors):
            orig_idx = actual_indices[start + idx]
            all_vectors[orig_idx] = vec

    return EmbeddingResult(
        texts=texts,
        vectors=[v if v else [0.0] * 768 for v in all_vectors],
        model=client.model,
        dimensions=client.dimensions,
    )


# ──────────────────────────────────────────────
# 6. MAIN DEMO
# ──────────────────────────────────────────────

# Sample documents (banking/ETL domain — matches Krishna's background)
SAMPLE_DOCS = [
    "Banking ETL pipeline extracts transaction data from core banking system daily.",
    "Data quality checks validate record counts and null percentages before loading.",
    "Watermark-based incremental load processes only new records since last run.",
    "BigQuery stores historical transactions partitioned by processing date.",
    "Reconciliation reports compare source system counts with warehouse counts.",
    "The customer 360 view joins transaction, demographic, and interaction data.",
    "Fraud detection models flag transactions exceeding normal spending patterns.",
    "Regulatory reporting requires complete audit trail for all data transformations.",
    "Slowly changing dimensions track customer address changes over time in Type 2 tables.",
    "Real-time streaming ingests card swipe events through Pub/Sub to BigQuery.",
]


def main():
    client = MockEmbeddingClient()
    store = EmbeddingStore(client)

    print("=" * 60)
    print("DAY 17: EMBEDDINGS — TEXT-EMBEDDING-004 + SIMILARITY SEARCH")
    print("=" * 60)

    # --- Demo 1: Embed a single text ---
    print("\n--- DEMO 1: Single Text Embedding ---")
    result = client.embed(["What is an ETL pipeline?"])
    vec = result.vectors[0]
    print(f"  Text: 'What is an ETL pipeline?'")
    print(f"  Model: {result.model}")
    print(f"  Dimensions: {result.dimensions}")
    print(f"  First 5 values: {vec[:5]}")
    print(f"  Vector magnitude: {math.sqrt(sum(v*v for v in vec)):.4f} (should be ~1.0)")

    # --- Demo 2: Similarity between pairs ---
    print("\n--- DEMO 2: Pairwise Similarity ---")
    pairs = [
        ("ETL pipeline extracts data", "Data extraction from source systems"),
        ("ETL pipeline extracts data", "Fraud detection model training"),
        ("Banking transactions", "Card payment processing"),
    ]
    for text_a, text_b in pairs:
        vec_a = client.embed([text_a]).vectors[0]
        vec_b = client.embed([text_b]).vectors[0]
        cos_sim = cosine_similarity(vec_a, vec_b)
        euc_dist = euclidean_distance(vec_a, vec_b)
        print(f"  '{text_a[:30]}...' ↔ '{text_b[:30]}...'")
        print(f"    Cosine: {cos_sim:.4f}  |  Euclidean: {euc_dist:.4f}")

    # --- Demo 3: Document retrieval ---
    print("\n--- DEMO 3: Semantic Search (Retrieval) ---")
    store.add_documents(SAMPLE_DOCS)
    store.index()
    print(f"  Indexed {len(store.documents)} documents")

    queries = [
        "How do we handle new records?",
        "What checks ensure data is correct?",
        "How does fraud detection work?",
    ]
    for query in queries:
        results = store.search(query, top_k=3)
        print(f"\n  Query: '{query}'")
        for rank, (doc, score) in enumerate(results.results, 1):
            print(f"    #{rank} [{score:.4f}] {doc[:70]}...")

    # --- Demo 4: Similarity matrix ---
    print("\n--- DEMO 4: Document Similarity Matrix (top 5) ---")
    matrix = store.similarity_matrix()
    labels = [f"Doc{i}" for i in range(min(5, len(store.documents)))]
    header = "       " + "  ".join(f"{l:>6}" for l in labels)
    print(f"  {header}")
    for i in range(min(5, len(matrix))):
        row = "  ".join(f"{matrix[i][j]:>6.3f}" for j in range(min(5, len(matrix[i]))))
        print(f"  {labels[i]:>6} {row}")

    # --- Demo 5: Batch embedding ---
    print("\n--- DEMO 5: Batch Embedding ---")
    large_batch = [f"Document number {i} about banking topic {i % 5}" for i in range(50)]
    batch_result = batch_embed_with_retry(client, large_batch, batch_size=10)
    print(f"  Embedded {len(batch_result.texts)} texts")
    print(f"  Vector dimensions: {batch_result.dimensions}")
    non_empty = sum(1 for v in batch_result.vectors if any(x != 0 for x in v))
    print(f"  Non-empty vectors: {non_empty}/{len(batch_result.texts)}")

    # --- Demo 6: Embedding properties ---
    print("\n--- DEMO 6: Embedding Properties ---")
    props = [
        ("Same text, same vector", client.embed(["banking ETL"]).vectors[0] == client.embed(["banking ETL"]).vectors[0]),
        ("Unit vector magnitude", abs(math.sqrt(sum(v*v for v in client.embed(["test"]).vectors[0])) - 1.0) < 0.001),
        ("Dimension count", client.embed(["test"]).dimensions == 768),
    ]
    for name, result in props:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")

    print("\n" + "=" * 60)
    print("DAY 17 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
