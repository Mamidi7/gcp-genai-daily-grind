"""
Day 18: Chunking Strategies — 3 Approaches + Recall Comparison

Implement and compare:
1. Fixed-size chunking (character-based with overlap)
2. Sentence-based chunking (split on boundaries)
3. Semantic chunking (group by embedding similarity)

Then measure: which strategy gives better retrieval recall?

Interview question this answers:
  "How do you chunk documents for RAG? What tradeoffs do you consider?"
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

# Reuse Day 17 embedding infrastructure
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'day17'))
from solution import MockEmbeddingClient, cosine_similarity


# ──────────────────────────────────────────────
# 1. CORE TYPES
# ──────────────────────────────────────────────

@dataclass
class Chunk:
    """A single chunk of text."""
    text: str
    index: int
    char_count: int
    word_count: int
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChunkingResult:
    """Result from chunking a document."""
    strategy: str
    chunks: list[Chunk]
    total_chunks: int
    avg_chunk_size: float
    source_doc: str
    metadata: dict[str, Any] = field(default_factory=dict)


# ──────────────────────────────────────────────
# 2. STRATEGY 1: FIXED-SIZE CHUNKING
# ──────────────────────────────────────────────

def chunk_fixed_size(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    source: str = "",
) -> ChunkingResult:
    """
    Split text into fixed-size chunks with overlap.
    
    Simple and predictable. Production default for most RAG systems.
    
    Args:
        text: Input document
        chunk_size: Characters per chunk
        overlap: Characters to overlap between chunks
        source: Source document identifier
    """
    if chunk_size <= overlap:
        raise ValueError(f"chunk_size ({chunk_size}) must be > overlap ({overlap})")

    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(Chunk(
                text=chunk_text,
                index=idx,
                char_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                source=source,
                metadata={"start_char": start, "end_char": min(end, len(text))},
            ))
            idx += 1

        start += chunk_size - overlap

    return ChunkingResult(
        strategy="fixed_size",
        chunks=chunks,
        total_chunks=len(chunks),
        avg_chunk_size=sum(c.char_count for c in chunks) / len(chunks) if chunks else 0,
        source_doc=source,
        metadata={"chunk_size": chunk_size, "overlap": overlap},
    )


# ──────────────────────────────────────────────
# 3. STRATEGY 2: SENTENCE-BASED CHUNKING
# ──────────────────────────────────────────────

def split_sentences(text: str) -> list[str]:
    """Split text into sentences. Handles common abbreviations."""
    # Simple but effective sentence splitter
    # Handles: periods, exclamation, question marks
    # Doesn't handle: abbreviations perfectly (good enough for practice)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def chunk_sentences(
    text: str,
    target_size: int = 500,
    source: str = "",
) -> ChunkingResult:
    """
    Split text into chunks based on sentence boundaries.
    
    Groups sentences until target_size is reached.
    Never cuts a sentence in half.
    """
    sentences = split_sentences(text)
    if not sentences:
        return ChunkingResult(
            strategy="sentence", chunks=[], total_chunks=0,
            avg_chunk_size=0, source_doc=source,
        )

    chunks = []
    current_sentences: list[str] = []
    current_size = 0
    idx = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        if current_size + sentence_size > target_size and current_sentences:
            # Finalize current chunk
            chunk_text = " ".join(current_sentences)
            chunks.append(Chunk(
                text=chunk_text,
                index=idx,
                char_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                source=source,
                metadata={"sentence_count": len(current_sentences)},
            ))
            idx += 1
            current_sentences = []
            current_size = 0

        current_sentences.append(sentence)
        current_size += sentence_size + 1  # +1 for space

    # Don't forget the last chunk
    if current_sentences:
        chunk_text = " ".join(current_sentences)
        chunks.append(Chunk(
            text=chunk_text,
            index=idx,
            char_count=len(chunk_text),
            word_count=len(chunk_text.split()),
            source=source,
            metadata={"sentence_count": len(current_sentences)},
        ))

    return ChunkingResult(
        strategy="sentence",
        chunks=chunks,
        total_chunks=len(chunks),
        avg_chunk_size=sum(c.char_count for c in chunks) / len(chunks) if chunks else 0,
        source_doc=source,
        metadata={"target_size": target_size},
    )


# ──────────────────────────────────────────────
# 4. STRATEGY 3: SEMANTIC CHUNKING
# ──────────────────────────────────────────────

def chunk_semantic(
    text: str,
    embedding_client: MockEmbeddingClient,
    similarity_threshold: float = 0.5,
    min_chunk_size: int = 100,
    max_chunk_size: int = 1000,
    source: str = "",
) -> ChunkingResult:
    """
    Group sentences by embedding similarity.
    
    Algorithm:
    1. Split into sentences
    2. Embed each sentence
    3. Compare adjacent sentence similarity
    4. Start new chunk when similarity drops below threshold
    5. Enforce min/max chunk sizes
    """
    sentences = split_sentences(text)
    if not sentences:
        return ChunkingResult(
            strategy="semantic", chunks=[], total_chunks=0,
            avg_chunk_size=0, source_doc=source,
        )

    # Embed all sentences
    embeddings = embedding_client.embed(sentences).vectors

    # Compute adjacent similarities
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity(embeddings[i], embeddings[i + 1])
        similarities.append(sim)

    # Group into chunks based on similarity drops
    chunk_boundaries = [0]  # Start with first sentence
    for i, sim in enumerate(similarities):
        if sim < similarity_threshold:
            chunk_boundaries.append(i + 1)  # Start new chunk at next sentence
    chunk_boundaries.append(len(sentences))  # End boundary

    # Build chunks from boundaries
    chunks = []
    idx = 0
    for b in range(len(chunk_boundaries) - 1):
        start = chunk_boundaries[b]
        end = chunk_boundaries[b + 1]
        chunk_sentences_list = sentences[start:end]
        chunk_text = " ".join(chunk_sentences_list)

        if not chunk_text.strip():
            continue

        # Enforce max size — split if too large
        if len(chunk_text) > max_chunk_size:
            # Split at sentence boundaries within this chunk
            sub_text = ""
            for sent in chunk_sentences_list:
                if len(sub_text) + len(sent) > max_chunk_size and sub_text:
                    chunks.append(Chunk(
                        text=sub_text.strip(), index=idx,
                        char_count=len(sub_text.strip()),
                        word_count=len(sub_text.strip().split()),
                        source=source,
                        metadata={"method": "semantic_split"},
                    ))
                    idx += 1
                    sub_text = sent
                else:
                    sub_text += " " + sent
            if sub_text.strip():
                chunks.append(Chunk(
                    text=sub_text.strip(), index=idx,
                    char_count=len(sub_text.strip()),
                    word_count=len(sub_text.strip().split()),
                    source=source,
                    metadata={"method": "semantic_split"},
                ))
                idx += 1
        else:
            chunks.append(Chunk(
                text=chunk_text, index=idx,
                char_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                source=source,
                metadata={"method": "semantic", "sentence_count": end - start},
            ))
            idx += 1

    return ChunkingResult(
        strategy="semantic",
        chunks=chunks,
        total_chunks=len(chunks),
        avg_chunk_size=sum(c.char_count for c in chunks) / len(chunks) if chunks else 0,
        source_doc=source,
        metadata={"similarity_threshold": similarity_threshold, "adjacent_similarities": similarities},
    )


# ──────────────────────────────────────────────
# 5. COMPARISON ENGINE
# ──────────────────────────────────────────────

def compare_strategies(
    text: str,
    query: str,
    embedding_client: MockEmbeddingClient,
) -> dict[str, Any]:
    """Run all 3 strategies and compare retrieval quality."""
    strategies = {
        "fixed_size": chunk_fixed_size(text, chunk_size=500, overlap=50),
        "sentence": chunk_sentences(text, target_size=500),
        "semantic": chunk_semantic(text, embedding_client, similarity_threshold=0.5),
    }

    results = {}
    query_emb = embedding_client.embed([query]).vectors[0]

    for name, chunking_result in strategies.items():
        if not chunking_result.chunks:
            results[name] = {"top_similarity": 0, "chunk_count": 0, "avg_size": 0}
            continue

        # Embed all chunks and find best match
        chunk_texts = [c.text for c in chunking_result.chunks]
        chunk_embs = embedding_client.embed(chunk_texts).vectors

        sims = [cosine_similarity(query_emb, emb) for emb in chunk_embs]
        best_idx = max(range(len(sims)), key=lambda i: sims[i])

        results[name] = {
            "top_similarity": sims[best_idx],
            "top_chunk": chunk_texts[best_idx][:100] + "...",
            "chunk_count": chunking_result.total_chunks,
            "avg_size": round(chunking_result.avg_chunk_size, 1),
            "size_range": (
                min(c.char_count for c in chunking_result.chunks),
                max(c.char_count for c in chunking_result.chunks),
            ),
        }

    return results


# ──────────────────────────────────────────────
# 6. MAIN DEMO
# ──────────────────────────────────────────────

SAMPLE_DOCUMENT = """
Banking ETL Pipeline Architecture. The banking ETL pipeline extracts transaction data from the core banking system every day at 2 AM UTC. The extraction phase connects to the OLTP database using JDBC and pulls all records modified since the last watermark timestamp. 

Data quality validation occurs immediately after extraction. The system checks record counts against expected ranges, validates null percentages for critical fields like account_number and transaction_amount, and flags any records with future-dated timestamps. Records that fail validation are quarantined in a rejection table with a detailed error code.

The transformation phase applies business rules. Currency amounts are standardized to USD using daily exchange rates from the Federal Reserve API. Account identifiers are anonymized using a consistent hash function for GDPR compliance. Duplicate transactions are detected using a fuzzy matching algorithm that compares amount, timestamp, and merchant across a 24-hour window.

Loading into the data warehouse uses a merge operation. New records are inserted, existing records are updated if any fields changed, and slowly changing dimensions track address and contact changes using Type 2 methodology with effective dates. The entire pipeline is idempotent — running it twice produces the same result.

Monitoring and alerting are built into every stage. Cloud Logging captures structured JSON entries with trace IDs for end-to-end tracking. Error rates above 0.1% trigger PagerDuty alerts. Daily reconciliation compares source system record counts with warehouse counts and generates a variance report. Any variance above 0.01% requires manual investigation before the next business day.

The pipeline processes approximately 2.3 million transactions daily with a median latency of 45 minutes end-to-end. Peak volumes during month-end processing can reach 8 million transactions, requiring auto-scaling of the Dataflow workers from 4 to 16 instances.
"""


def main():
    client = MockEmbeddingClient()

    print("=" * 60)
    print("DAY 18: CHUNKING STRATEGIES — 3 APPROACHES")
    print("=" * 60)

    # --- Demo 1: Fixed-size chunking ---
    print("\n--- STRATEGY 1: Fixed-Size Chunking ---")
    fixed = chunk_fixed_size(SAMPLE_DOCUMENT, chunk_size=300, overlap=30, source="etl_doc")
    print(f"  Chunks: {fixed.total_chunks}")
    print(f"  Avg size: {fixed.avg_chunk_size:.0f} chars")
    for c in fixed.chunks[:3]:
        print(f"  Chunk {c.index}: {c.char_count} chars, {c.word_count} words")
        print(f"    Preview: {c.text[:80]}...")

    # --- Demo 2: Sentence-based chunking ---
    print("\n--- STRATEGY 2: Sentence-Based Chunking ---")
    sent = chunk_sentences(SAMPLE_DOCUMENT, target_size=300, source="etl_doc")
    print(f"  Chunks: {sent.total_chunks}")
    print(f"  Avg size: {sent.avg_chunk_size:.0f} chars")
    for c in sent.chunks[:3]:
        print(f"  Chunk {c.index}: {c.char_count} chars, {c.word_count} words, {c.metadata.get('sentence_count', '?')} sentences")
        print(f"    Preview: {c.text[:80]}...")

    # --- Demo 3: Semantic chunking ---
    print("\n--- STRATEGY 3: Semantic Chunking ---")
    sem = chunk_semantic(SAMPLE_DOCUMENT, client, similarity_threshold=0.5, source="etl_doc")
    print(f"  Chunks: {sem.total_chunks}")
    print(f"  Avg size: {sem.avg_chunk_size:.0f} chars")
    if sem.metadata.get("adjacent_similarities"):
        sims = sem.metadata["adjacent_similarities"]
        print(f"  Adjacent similarity range: {min(sims):.3f} to {max(sims):.3f}")
    for c in sem.chunks[:3]:
        print(f"  Chunk {c.index}: {c.char_count} chars, {c.word_count} words")
        print(f"    Preview: {c.text[:80]}...")

    # --- Demo 4: Strategy comparison ---
    print("\n--- DEMO 4: Retrieval Quality Comparison ---")
    queries = [
        "How does data quality validation work?",
        "What is the daily transaction volume?",
        "How are duplicates detected?",
    ]
    for query in queries:
        print(f"\n  Query: '{query}'")
        comparison = compare_strategies(SAMPLE_DOCUMENT, query, client)
        for strategy, data in comparison.items():
            print(f"    {strategy:>12}: top_sim={data['top_similarity']:.4f}, chunks={data['chunk_count']}, avg_size={data['avg_size']}")

    # --- Demo 5: Chunk size impact ---
    print("\n--- DEMO 5: Chunk Size Impact on Fixed-Size ---")
    for size in [100, 200, 500, 1000]:
        result = chunk_fixed_size(SAMPLE_DOCUMENT, chunk_size=size, overlap=size // 10)
        print(f"  Size {size:4d}: {result.total_chunks} chunks, avg={result.avg_chunk_size:.0f} chars")

    print("\n" + "=" * 60)
    print("DAY 18 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
