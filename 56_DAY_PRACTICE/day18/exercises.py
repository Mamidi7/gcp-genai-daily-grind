"""
Day 18 Exercises: Chunking Strategies Practice
"""

# ── Exercise 1: Implement recursive character chunking ──

def chunk_recursive(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    separators: list[str] = None,
) -> list[str]:
    """
    TODO: Split text using a hierarchy of separators.
    
    Try splitting by "\n\n" first. If chunks are still too big,
    try "\n", then ". ", then " ", then characters.
    
    This is what LangChain's RecursiveCharacterTextSplitter does.
    """
    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]
    # TODO: implement
    return []


# ── Exercise 2: Overlap analysis ──

def measure_overlap(chunks: list[str]) -> list[dict]:
    """
    TODO: Measure the overlap between adjacent chunks.
    
    For each pair of adjacent chunks, compute:
    - How many words are shared between chunk[i] end and chunk[i+1] start
    - The Jaccard similarity of their word sets
    
    Returns: list of {"shared_words": int, "jaccard": float} per pair
    """
    # TODO: implement
    return []


# ── Exercise 3: Find optimal chunk size ──

def find_optimal_chunk_size(
    text: str,
    query: str,
    embed_func,
    sizes: list[int] = [100, 200, 300, 500, 800, 1000],
) -> dict:
    """
    TODO: Test different chunk sizes and report retrieval quality.
    
    For each size:
    1. Chunk the text using fixed-size strategy
    2. Embed all chunks + query
    3. Find best matching chunk
    4. Record similarity score
    
    Returns: {"best_size": int, "results": [{size, similarity, chunk_count}]}
    """
    # TODO: implement
    return {"best_size": 0, "results": []}


# ── Exercise 4: Interview Questions ──

INTERVIEW_QUESTIONS = """
1. "What chunk size do you use and why?"
   Answer in 3 lines.

2. "How do you handle a document that's mostly code mixed with prose?"
   Answer in 3 lines.

3. "What's wrong with using a single chunk for an entire document?"
   Answer in 3 lines.
"""

MY_ANSWERS = """
TODO: Write your answers.
"""


if __name__ == "__main__":
    print("Day 18 Exercises — complete the TODOs above.")
