# Day 16 Interview Pack — Structured Output

## 30-Second Version
"I built a structured output layer for LLM responses using Gemini's JSON mode and Pydantic validation. It extracts JSON from messy LLM output, validates against typed schemas, and retries with error feedback on failure. Parse failure rate dropped from 15% to under 1%."

---

## 90-Second STAR Answer

**Situation:** In my AI pipeline project, LLM outputs were randomly breaking downstream processing because responses weren't consistently parseable.

**Task:** I needed to guarantee that every LLM response could be converted into a typed Python object for agent routing and data extraction.

**Action:** I built a 3-layer validation pipeline:
1. **Extraction layer**: Regex-based JSON extractor that handles markdown fences, preamble text, and trailing characters
2. **Parse layer**: json.loads with clear error messages showing exact failure position
3. **Validation layer**: Pydantic models with Field constraints (confidence 0-1, non-empty strings, min/max lengths)
On failure, the error message is fed back into a retry with the JSON schema included.

**Result:** Parse failure rate dropped from ~15% to under 1%. The retry logic means the system self-heals — most failures resolve in 1 retry. The Pydantic schemas also serve as living documentation of our data contracts.

---

## 3-Minute Technical Deep Dive

### The Problem Space
LLMs are text generators, not JSON APIs. Even with JSON mode enabled, you get:
- Markdown-wrapped output: ` ```json {...} ``` `
- Schema violations: `confidence: 1.5` when max is 1.0
- Missing fields: omitting `reasoning` when the prompt was vague
- Empty responses: timeouts, rate limits

### The Architecture
```
Prompt + Schema Description
         │
         ▼
    ┌─────────┐
    │  Gemini  │  ← response_mime_type="application/json"
    └────┬────┘
         │ raw text
         ▼
    ┌──────────────┐
    │ extract_json │  ← regex: strip fences, find { } blocks
    └────┬─────────┘
         │ clean JSON string
         ▼
    ┌──────────────┐
    │ json.loads   │  ← first gate: syntactic validity
    └────┬─────────┘
         │ dict
         ▼
    ┌──────────────┐
    │ Pydantic     │  ← second gate: semantic validity
    │ validate     │     field types, ranges, required fields
    └────┬─────────┘
         │ typed BaseModel object
         ▼
    Application Code ✓
```

### Why Two Validation Gates?
- json.loads catches SYNTAX errors (missing quotes, trailing commas)
- Pydantic catches SEMANTIC errors (wrong type, out of range, missing required)
- You need both because valid JSON ≠ valid data

### The Retry Loop
On parse failure, the retry adds the error to the prompt:
```
"Your previous response failed validation: 
 confidence: Input should be less than or equal to 1.0
 You MUST return valid JSON matching this schema: {...}"
```
This works because LLMs are good at fixing specific errors when told what went wrong.

### Production Considerations
- **Token cost**: Each retry costs tokens. Max 3 retries is the sweet spot.
- **Latency**: Retries add 1-3 seconds each. Track `attempts` metric.
- **Monitoring**: Log `metadata.attempts` — if average > 1.5, your prompt needs improvement.
- **Fallback**: If all retries fail, return a default safe response, never crash.

---

## Common Interview Questions

**Q: What if Gemini doesn't support JSON mode?**
A: The extract_json() function handles non-JSON-mode output. It finds JSON in mixed text. JSON mode is a preference, not a requirement.

**Q: How do you handle schema changes?**
A: Version your Pydantic models (V1, V2). Write migration functions. Store raw LLM output alongside parsed output so you can re-parse later.

**Q: What about performance?**
A: The extract + parse + validate pipeline adds <1ms. Retries are the expensive part — each adds one API call. Track retry rate as a health metric.
