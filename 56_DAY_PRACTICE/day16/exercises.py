"""
Day 16 Exercises: Structured Output Practice

Complete each function. Run `python exercises.py` to check your work.
"""

from pydantic import BaseModel, Field
import json


# ── Exercise 1: Define a Pydantic model for a product review ──

class ProductReview(BaseModel):
    """TODO: Define fields for a product review.
    Requirements:
    - product_name: str (min 1 char)
    - rating: int (1-5)
    - pros: list of strings (at least 1)
    - cons: list of strings (can be empty)
    - would_recommend: bool
    - summary: str (max 200 chars)
    """
    # TODO: Define your fields here
    pass


# ── Exercise 2: Build a JSON extractor ──

def extract_json_from_llm_output(text: str) -> str:
    """
    TODO: Extract clean JSON from messy LLM output.
    
    Handle these cases:
    1. Clean JSON: '{"a": 1}' → '{"a": 1}'
    2. Markdown fenced: '```json\n{"a": 1}\n```' → '{"a": 1}'
    3. With preamble: 'Here is the JSON:\n{"a": 1}' → '{"a": 1}'
    4. Array response: '[{"a": 1}, {"b": 2}]' → '[{"a": 1}, {"b": 2}]'
    
    Hint: Use regex. Think about what makes JSON distinctive.
    """
    # TODO: implement
    return text


# ── Exercise 3: Build a retry wrapper ──

def call_with_retry(
    llm_func,
    prompt: str,
    schema: type[BaseModel],
    max_retries: int = 3,
) -> BaseModel:
    """
    TODO: Call llm_func(prompt) -> str, parse result into schema.
    On failure, retry with error feedback added to prompt.
    
    llm_func signature: (prompt: str) -> str
    
    Steps:
    1. Call llm_func with prompt
    2. Try to parse with schema.model_validate_json()
    3. If fail, add error message to prompt and retry
    4. If max_retries exhausted, raise the error
    """
    # TODO: implement
    pass


# ── Exercise 4: Schema migration ──

class SentimentV1(BaseModel):
    label: str  # "positive", "negative", "neutral"
    score: float


class SentimentV2(BaseModel):
    label: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=10)
    detected_phrases: list[str] = Field(default_factory=list)


def migrate_v1_to_v2(v1_output: dict) -> dict:
    """
    TODO: Convert a V1 sentiment output to V2 format.
    
    v1_output: {"label": "positive", "score": 0.85}
    v2_output: {"label": "positive", "confidence": 0.85, 
                "reasoning": "migrated from v1", "detected_phrases": []}
    
    Handle: score outside 0-1 range, missing fields, extra fields.
    """
    # TODO: implement
    return {}


# ── Exercise 5: Interview Question ──

INTERVIEW_QUESTION = """
Q: "How do you handle LLM structured output in production?"

Write your 90-second answer below (6-8 lines).
Include: what breaks, how you fix it, what you monitor.

Your answer:
"""

# Write your answer here
MY_ANSWER = """
TODO: Write your interview answer here.
"""


if __name__ == "__main__":
    print("Day 16 Exercises")
    print("=" * 40)
    
    # Test Exercise 1
    print("\n--- Exercise 1: ProductReview model ---")
    try:
        review = ProductReview(
            product_name="Widget Pro",
            rating=4,
            pros=["Fast", "Reliable"],
            cons=["Expensive"],
            would_recommend=True,
            summary="Good product overall",
        )
        print(f"  Model works: {review.model_dump_json()}")
    except Exception as e:
        print(f"  Model NOT defined yet: {e}")
    
    # Test Exercise 2
    print("\n--- Exercise 2: JSON extractor ---")
    test_cases = [
        ('{"a": 1}', "clean JSON"),
        ('```json\n{"a": 1}\n```', "markdown fenced"),
        ('Result:\n{"a": 1}', "with preamble"),
    ]
    for raw, desc in test_cases:
        result = extract_json_from_llm_output(raw)
        try:
            json.loads(result)
            print(f"  {desc}: PASS")
        except:
            print(f"  {desc}: FAIL — got '{result}'")
    
    # Test Exercise 4
    print("\n--- Exercise 4: V1→V2 migration ---")
    v1 = {"label": "positive", "score": 0.85}
    v2 = migrate_v1_to_v2(v1)
    try:
        validated = SentimentV2(**v2)
        print(f"  Migration works: {validated.model_dump_json()}")
    except Exception as e:
        print(f"  Migration NOT implemented: {e}")
    
    print("\nDone! Complete the TODOs above.")
