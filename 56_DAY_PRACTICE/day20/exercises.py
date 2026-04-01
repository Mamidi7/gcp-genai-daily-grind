"""
Day 20 Exercises: Eval Harness Practice
"""


# ── Exercise 1: Add regression detection ──

def detect_regressions(
    current_results: list[dict],
    previous_results: list[dict],
) -> list[dict]:
    """
    TODO: Compare two eval runs and find regressions.
    
    A regression is when a case that was 'correct' becomes 'partial' or 'incorrect'.
    
    Returns: list of {"test_id": str, "previous": str, "current": str, "regression": bool}
    """
    # TODO: implement
    return []


# ── Exercise 2: Build a smoke test subset ──

def create_smoke_test(full_suite: list, n: int = 3) -> list:
    """
    TODO: Select n test cases for quick smoke testing.
    
    Criteria:
    - Must include at least 1 safety case
    - Must include at least 1 factual case
    - Should cover different difficulties
    
    Returns: subset of test cases
    """
    # TODO: implement
    return []


# ── Exercise 3: Statistical significance ──

def is_improvement_significant(
    before: list[str],  # list of "correct"/"partial"/"incorrect"
    after: list[str],
    confidence: float = 0.95,
) -> dict:
    """
    TODO: Determine if improvement between two runs is statistically significant.
    
    Simple version: compare accuracy percentages.
    Advanced: use McNemar's test for paired binary outcomes.
    
    Returns: {"significant": bool, "p_value": float, "confidence": float}
    """
    # TODO: implement
    return {"significant": False, "p_value": 1.0, "confidence": confidence}


# ── Exercise 4: Interview Questions ──

INTERVIEW_QUESTIONS = """
1. "What accuracy do you need before deploying to production?"
   Answer in 3 lines.

2. "How do you handle false positives in your eval (correct but actually wrong)?"
   Answer in 3 lines.

3. "What's the minimum viable eval suite for a new LLM feature?"
   Answer in 3 lines.
"""

MY_ANSWERS = """
TODO: Write your answers.
"""


if __name__ == "__main__":
    print("Day 20 Exercises — complete the TODOs above.")
