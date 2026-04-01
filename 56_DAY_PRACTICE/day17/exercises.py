"""
Day 17 Exercises: Embeddings Practice

Complete each function. Run `python exercises.py` to check your work.
"""

import math


# ── Exercise 1: Implement cosine similarity from scratch ──

def my_cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    TODO: Implement cosine similarity without using any library.
    
    Formula: cos(a,b) = (a · b) / (|a| * |b|)
    where a · b = sum(a[i] * b[i])
    and |a| = sqrt(sum(a[i]^2))
    
    Handle: zero vectors (return 0.0), different lengths (raise ValueError)
    """
    # TODO: implement
    pass


# ── Exercise 2: Top-k retrieval ──

def find_top_k(
    query_vector: list[float],
    document_vectors: list[tuple[str, list[float]]],  # (doc_id, vector)
    k: int = 5,
) -> list[tuple[str, float]]:
    """
    TODO: Find the k most similar documents to query_vector.
    
    Returns: list of (doc_id, similarity_score) sorted by score descending.
    
    Steps:
    1. Compute cosine similarity between query and each doc
    2. Sort by similarity descending
    3. Return top k
    """
    # TODO: implement
    return []


# ── Exercise 3: Batch chunking for embedding ──

def prepare_for_embedding(
    texts: list[str],
    max_tokens: int = 500,
) -> list[list[str]]:
    """
    TODO: Split a list of texts into batches for embedding API.
    
    Rules:
    - Each batch should have total word count ≤ max_tokens
    - No empty texts in any batch
    - Preserve original order
    
    Returns: list of batches, where each batch is a list of strings
    
    Example:
      texts = ["a b c", "d e", "f g h i j k", "l m"]
      max_tokens = 5
      → [["a b c", "d e"], ["f g h i j k"], ["l m"]]
    """
    # TODO: implement
    return []


# ── Exercise 4: Similarity threshold filter ──

def filter_by_similarity(
    query_vector: list[float],
    candidates: list[tuple[str, list[float]]],
    threshold: float = 0.7,
) -> list[tuple[str, float]]:
    """
    TODO: Return only candidates above similarity threshold.
    
    This is what production RAG does — don't return garbage matches.
    
    Returns: list of (doc_id, score) where score >= threshold, sorted descending.
    """
    # TODO: implement
    return []


# ── Exercise 5: Conceptual Questions ──

INTERVIEW_QUESTIONS = """
Answer these in your own words (2-3 lines each):

1. Why use cosine similarity instead of Euclidean distance for embeddings?
   
2. What happens to embedding quality when you truncate text?
   
3. Why are embeddings 768 dimensions? Why not 10 or 10000?
   
4. When would keyword search be better than embedding search?
"""

MY_ANSWERS = """
TODO: Write your answers here.
"""


if __name__ == "__main__":
    print("Day 17 Exercises")
    print("=" * 40)
    
    # Test Exercise 1
    print("\n--- Exercise 1: Cosine Similarity ---")
    try:
        a = [1.0, 0.0, 0.0]
        b = [0.0, 1.0, 0.0]
        result = my_cosine_similarity(a, b)
        expected = 0.0
        if result is not None and abs(result - expected) < 0.001:
            print(f"  Orthogonal vectors: PASS ({result:.4f})")
        else:
            print(f"  Orthogonal vectors: expected 0.0, got {result}")
    except Exception as e:
        print(f"  NOT implemented: {e}")
    
    # Test Exercise 2
    print("\n--- Exercise 2: Top-k Retrieval ---")
    try:
        query = [1.0, 0.0]
        docs = [
            ("doc1", [0.9, 0.1]),
            ("doc2", [0.0, 1.0]),
            ("doc3", [0.8, 0.2]),
            ("doc4", [0.1, 0.9]),
        ]
        top = find_top_k(query, docs, k=2)
        if len(top) == 2:
            print(f"  Top 2: {top}")
            print(f"  PASS" if top[0][0] in ("doc1", "doc3") else "  Check ordering")
        else:
            print(f"  Expected 2 results, got {len(top)}")
    except Exception as e:
        print(f"  NOT implemented: {e}")
    
    # Test Exercise 3
    print("\n--- Exercise 3: Batch Preparation ---")
    try:
        texts = ["a b c", "d e", "f g h i j k", "l m"]
        batches = prepare_for_embedding(texts, max_tokens=5)
        total_texts = sum(len(b) for b in batches)
        print(f"  {len(batches)} batches, {total_texts} total texts")
        print(f"  PASS" if total_texts == 4 else "  Some texts lost")
    except Exception as e:
        print(f"  NOT implemented: {e}")
    
    print("\nDone! Complete the TODOs above.")
