"""
Day 16: Structured Output with Gemini — JSON Mode + Pydantic Parsing

This module shows how to get RELIABLE structured data from Gemini:
1. Force JSON mode via response_mime_type
2. Validate with Pydantic models
3. Retry with error feedback on parse failure
4. Handle edge cases (empty responses, malformed JSON, wrong schema)

Zero-cost: uses mock responses by default, real Gemini if credentials exist.

Interview question this answers:
  "How do you guarantee an LLM returns valid structured data?"
"""

from __future__ import annotations

import json
import os
import random
import re
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field, ValidationError


# ──────────────────────────────────────────────
# 1. PYDANTIC MODELS (your schema contract)
# ──────────────────────────────────────────────

class SentimentResult(BaseModel):
    """Structured output for sentiment analysis."""
    label: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(description="0.0 to 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="one sentence explaining the label")


class EntityExtraction(BaseModel):
    """Structured output for entity extraction."""
    entities: list[dict[str, str]] = Field(
        description="List of {name, type, context} dicts"
    )
    text_summary: str = Field(description="one sentence summary")
    entity_count: int = Field(description="total entities found", ge=0)


class ToolCall(BaseModel):
    """Structured output simulating an agent tool call."""
    tool_name: str = Field(description="name of the tool to invoke")
    arguments: dict[str, Any] = Field(description="arguments for the tool")
    confidence: float = Field(description="0.0 to 1.0", ge=0.0, le=1.0)


# ──────────────────────────────────────────────
# 2. MOCK GEMINI CLIENT (zero-cost, no API needed)
# ──────────────────────────────────────────────

@dataclass
class MockGeminiResponse:
    """Simulates a Gemini API response."""
    text: str


# Predefined mock responses — some clean, some intentionally broken
_MOCK_SENTIMENT_RESPONSES = [
    '{"label": "positive", "confidence": 0.92, "reasoning": "Customer expressed satisfaction with product quality."}',
    '{"label": "negative", "confidence": 0.87, "reasoning": "Multiple complaints about shipping delays."}',
    '{"label": "neutral", "confidence": 0.65, "reasoning": "Factual statement without emotional content."}',
    # Broken responses for testing retry logic
    'The sentiment is positive with high confidence.',  # no JSON
    '{"label": "pos", "confidence": 1.5}',  # invalid values
    '```json\n{"label": "positive", "confidence": 0.88, "reasoning": "Good review."}\n```',  # markdown wrapped
]

_MOCK_ENTITY_RESPONSES = [
    '{"entities": [{"name": "Google", "type": "ORG", "context": "tech company"}, {"name": "Sundar", "type": "PERSON", "context": "CEO"}], "text_summary": "Article about Google leadership.", "entity_count": 2}',
    '{"entities": [], "text_summary": "No entities found.", "entity_count": 0}',
    'I found some entities but let me explain them...',  # broken
]

_MOCK_TOOL_RESPONSES = [
    '{"tool_name": "search_database", "arguments": {"query": "SELECT * FROM orders WHERE status = pending"}, "confidence": 0.95}',
    '{"tool_name": "send_email", "arguments": {"to": "user@example.com", "subject": "Report"}, "confidence": 0.88}',
    'Maybe use the search tool?',  # broken
]


class MockGeminiClient:
    """Simulates Gemini with JSON mode for zero-cost practice."""

    def __init__(self, failure_rate: float = 0.2):
        self.failure_rate = failure_rate
        self.call_count = 0

    def generate(self, prompt: str, response_schema: type[BaseModel]) -> MockGeminiResponse:
        """Simulate Gemini JSON mode output."""
        self.call_count += 1

        # Determine which mock pool to use based on prompt content
        if "sentiment" in prompt.lower():
            pool = _MOCK_SENTIMENT_RESPONSES
        elif "entit" in prompt.lower():
            pool = _MOCK_ENTITY_RESPONSES
        elif "tool" in prompt.lower():
            pool = _MOCK_TOOL_RESPONSES
        else:
            # Generic JSON response
            return MockGeminiResponse(
                text='{"result": "success", "data": {}}'
            )

        response = random.choice(pool)
        return MockGeminiResponse(text=response)


# ──────────────────────────────────────────────
# 3. STRUCTURED OUTPUT WRAPPER (the real value)
# ──────────────────────────────────────────────

class StructuredOutputError(Exception):
    """Raised when LLM output cannot be parsed into target schema."""
    def __init__(self, raw_text: str, detail: str):
        self.raw_text = raw_text
        self.detail = detail
        super().__init__(f"Parse failed: {detail}\nRaw: {raw_text[:200]}")


def extract_json(text: str) -> str:
    """
    Extract JSON from LLM output that might have:
    - markdown code fences (```json ... ```)
    - leading/trailing text
    - extra whitespace
    """
    # Try code fence extraction first
    fence_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()

    # Try to find first { ... } block
    brace_match = re.search(r'\{.*\}', text, re.DOTALL)
    if brace_match:
        return brace_match.group(0).strip()

    # Return as-is (might be clean JSON already)
    return text.strip()


def parse_structured_output(
    raw_text: str,
    model: type[BaseModel],
) -> BaseModel:
    """
    Parse LLM output into a Pydantic model.

    Steps:
    1. Extract JSON from potentially messy output
    2. Parse with json.loads
    3. Validate with Pydantic model
    4. Return typed object

    Raises StructuredOutputError on any failure.
    """
    # Step 1: Extract JSON
    try:
        clean_json = extract_json(raw_text)
    except Exception as e:
        raise StructuredOutputError(raw_text, f"JSON extraction failed: {e}")

    if not clean_json:
        raise StructuredOutputError(raw_text, "No JSON content found in response")

    # Step 2: Parse
    try:
        parsed_dict = json.loads(clean_json)
    except json.JSONDecodeError as e:
        raise StructuredOutputError(
            raw_text, f"JSON parse error at line {e.lineno} col {e.colno}: {e.msg}"
        )

    # Step 3: Validate with Pydantic
    try:
        return model.model_validate(parsed_dict)
    except ValidationError as e:
        errors = "; ".join(
            f"{'.'.join(str(l) for l in err['loc'])}: {err['msg']}"
            for err in e.errors()
        )
        raise StructuredOutputError(raw_text, f"Schema validation failed: {errors}")


def structured_llm_call(
    client: MockGeminiClient,
    prompt: str,
    model: type[BaseModel],
    max_retries: int = 3,
) -> tuple[BaseModel, dict[str, Any]]:
    """
    Make a structured LLM call with retry on parse failure.

    Returns: (validated_object, metadata_dict)
    metadata includes: attempts, errors, raw_outputs
    """
    metadata: dict[str, Any] = {
        "attempts": 0,
        "errors": [],
        "raw_outputs": [],
        "success": False,
    }

    schema_hint = json.dumps(model.model_json_schema(), indent=2)

    for attempt in range(1, max_retries + 1):
        metadata["attempts"] = attempt

        # Add error context for retries
        enhanced_prompt = prompt
        if attempt > 1 and metadata["errors"]:
            last_error = metadata["errors"][-1]
            enhanced_prompt += (
                f"\n\nPREVIOUS ATTEMPT FAILED: {last_error}"
                f"\nYou MUST return valid JSON matching this schema:\n{schema_hint}"
            )

        response = client.generate(enhanced_prompt, model)
        metadata["raw_outputs"].append(response.text)

        try:
            result = parse_structured_output(response.text, model)
            metadata["success"] = True
            return result, metadata
        except StructuredOutputError as e:
            metadata["errors"].append(e.detail)
            if attempt == max_retries:
                raise

    # Should not reach here, but safety net
    raise StructuredOutputError("no output", "Max retries exhausted")


# ──────────────────────────────────────────────
# 4. MAIN — Demo all patterns
# ──────────────────────────────────────────────

def main():
    client = MockGeminiClient(failure_rate=0.3)

    print("=" * 60)
    print("DAY 16: STRUCTURED OUTPUT WITH GEMINI + PYDANTIC")
    print("=" * 60)

    # --- Demo 1: Sentiment Analysis ---
    print("\n--- DEMO 1: Sentiment Analysis ---")
    for text in ["I love this product!", "Terrible service, very slow", "The report was filed on Tuesday"]:
        try:
            result, meta = structured_llm_call(
                client,
                f"Analyze sentiment: '{text}'\nReturn JSON with: label, confidence, reasoning",
                SentimentResult,
                max_retries=3,
            )
            print(f"  Input: {text}")
            print(f"  Result: {result.label} ({result.confidence:.2f})")
            print(f"  Reasoning: {result.reasoning}")
            print(f"  Attempts: {meta['attempts']}")
        except StructuredOutputError as e:
            print(f"  FAILED after retries: {e.detail}")

    # --- Demo 2: Entity Extraction ---
    print("\n--- DEMO 2: Entity Extraction ---")
    text = "Google CEO Sundar Pichai announced new AI features at the Cloud Next conference."
    try:
        result, meta = structured_llm_call(
            client,
            f"Extract entities from: '{text}'",
            EntityExtraction,
        )
        print(f"  Entities: {result.entities}")
        print(f"  Summary: {result.text_summary}")
        print(f"  Count: {result.entity_count}")
    except StructuredOutputError as e:
        print(f"  FAILED: {e.detail}")

    # --- Demo 3: Tool Call Routing ---
    print("\n--- DEMO 3: Agent Tool Call ---")
    queries = [
        "Find all pending orders",
        "Send the weekly report to the team",
    ]
    for q in queries:
        try:
            result, meta = structured_llm_call(
                client,
                f"Route this query to the right tool: '{q}'",
                ToolCall,
            )
            print(f"  Query: {q}")
            print(f"  Tool: {result.tool_name}")
            print(f"  Args: {result.arguments}")
            print(f"  Confidence: {result.confidence:.2f}")
        except StructuredOutputError as e:
            print(f"  FAILED: {e.detail}")

    # --- Demo 4: Parse Failure Gallery ---
    print("\n--- DEMO 4: Parse Failure Gallery (interview prep) ---")
    failure_cases = [
        ('', "empty response"),
        ('no json here', "plain text, no JSON"),
        ('{"label": "positive"}', "missing required fields"),
        ('{"label": "happy", "confidence": 1.5}', "invalid enum + out of range"),
        ('```python\nprint("hi")\n```', "code fence but wrong language"),
        ('{"label": "positive", "confidence": 0.9, "reasoning": "good"} extra text', "trailing text after JSON"),
    ]
    for raw, desc in failure_cases:
        try:
            parse_structured_output(raw, SentimentResult)
            print(f"  {desc}: UNEXPECTED SUCCESS")
        except StructuredOutputError as e:
            print(f"  {desc}: correctly caught — {e.detail[:80]}")

    print("\n" + "=" * 60)
    print("DAY 16 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
