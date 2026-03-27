# Day 15 Interview Pack — Wrapper vs Direct SDK

## 30-Second
"I built a minimal Python LLM wrapper that standardizes model output into a typed shape and validates parse safety. It separates transient upstream retries from schema parsing so failures are easier to diagnose."

## 90-Second STAR
**Situation:** Direct SDK calls returned variable text formats, causing brittle downstream parsing.

**Task:** Create a small wrapper that returns predictable output and handles failure paths cleanly.

**Action:**
1. Designed a wrapper API: `ask(prompt) -> WrapperResponse`.
2. Defined strict output contract (`answer`, `confidence`, `source`).
3. Added JSON parsing + validation with explicit `ParseError`.
4. Added timeout and retry placeholders for transient upstream issues.
5. Added local smoke tests with fake client modes (`ok`, `transient`, `bad_json`).

**Result:** Callers now receive stable structured responses, parse failures fail fast with clear errors, and retry behavior is isolated from schema validation.

## 3-Minute Walkthrough
- **Input:** prompt text from API/service layer.
- **Inside wrapper:** call upstream client, apply timeout/retry, parse JSON, validate schema and ranges.
- **Output:** typed response object usable by API/business logic.
- **Failure separation:** upstream instability -> retry/timeout path; malformed payload -> parse path.
- **Design benefit:** easier testing, clearer observability, reusable integration point across providers.
