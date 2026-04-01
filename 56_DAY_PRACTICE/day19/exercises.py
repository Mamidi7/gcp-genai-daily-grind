"""
Day 19 Exercises: Eval Suite Practice
"""


# ── Exercise 1: Write 3 test cases for a RAG system about cooking ──

def create_cooking_test_cases():
    """
    TODO: Create 3 test cases for a cooking Q&A system.
    
    Each case needs: question, ground_truth, key_facts (3-5), forbidden_patterns.
    Include: 1 factual, 1 edge case, 1 safety (e.g., food allergy).
    
    Return list of dicts with those fields.
    """
    return []


# ── Exercise 2: Implement semantic scoring ──

def semantic_score(response: str, ground_truth: str) -> float:
    """
    TODO: Score response similarity to ground truth.
    
    Simple version: word overlap ratio.
    Advanced version: use embeddings (Day 17).
    
    Returns: float 0.0 to 1.0
    """
    # TODO: implement
    return 0.0


# ── Exercise 3: Eval coverage analysis ──

def analyze_test_coverage(test_cases: list[dict]) -> dict:
    """
    TODO: Analyze what your test suite covers and what it misses.
    
    Check:
    - Are all categories represented? (factual, edge_case, safety, adversarial)
    - Are difficulties balanced? (easy, medium, hard)
    - Are key fact counts reasonable? (2-6 per case)
    - Any overlap in questions? (similar questions test different things)
    
    Returns: {"coverage_score": float, "gaps": [str], "suggestions": [str]}
    """
    # TODO: implement
    return {"coverage_score": 0, "gaps": [], "suggestions": []}


# ── Exercise 4: Interview Questions ──

INTERVIEW_QUESTIONS = """
1. "What makes a good eval test case?"
   Answer in 3 lines.

2. "How many test cases do you need?"
   Answer in 3 lines.

3. "How do you prevent the eval from gaming itself?"
   Answer in 3 lines.
"""

MY_ANSWERS = """
TODO: Write your answers.
"""


if __name__ == "__main__":
    print("Day 19 Exercises — complete the TODOs above.")
