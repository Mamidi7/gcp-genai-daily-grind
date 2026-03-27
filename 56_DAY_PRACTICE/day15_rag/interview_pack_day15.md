# Day 15 Interview Pack — LLM Gateway Wrapper vs Direct SDK

## 30-Second
"I built a minimal Python LLM wrapper that standardizes model output into a typed shape and validates parse safety. It separates transient upstream retries from schema parsing so failures are easier to diagnose."

## ASCII Architecture
```text
API route / batch job
        |
        v
   LLM gateway wrapper
  request -> provider -> raw JSON
        |        ^
        v        |
 schema validation, retries, timeout, metadata
        |
        v
 typed response for app code
```

## 90-Second STAR
**Situation:** Direct SDK calls returned variable text formats, causing brittle downstream parsing.

**Task:** Create a small wrapper that returns predictable output and handles failure paths cleanly.

**Action:**
1. Designed a wrapper API: `ask(prompt) -> WrapperResponse`.
2. Defined strict output contract with metadata (`answer`, `confidence`, `source`, `request_id`, `latency_ms`, `provider`, `model`).
3. Added JSON parsing + validation with explicit `ParseError`.
4. Split timeout classification from generic upstream retry behavior.
5. Added local smoke tests with fake client modes (`ok`, `transient`, `bad_json`, `timeout`).

**Result:** Callers now receive stable structured responses, parse failures fail fast with clear errors, and retry behavior is isolated from schema validation.

## 3-Minute Walkthrough
- **Input:** prompt text from API/service layer.
- **Inside wrapper:** call upstream client, apply timeout/retry, parse JSON, validate schema and ranges.
- **Output:** typed response object with traceable metadata usable by API/business logic.
- **Failure separation:** upstream instability -> retry/timeout path; malformed payload -> parse path.
- **Design benefit:** easier testing, clearer observability, reusable integration point across providers.

## Why This Matters in Real Systems
The wrapper keeps provider-specific behavior out of route handlers, makes swap-outs easier later, and gives the team one place to enforce reliability and visibility.

## Common Interview Questions
**Why not call the SDK directly from each route?**
Because that duplicates retries, parsing, and error handling across the codebase. The wrapper creates one reliable integration boundary.

**Why separate parse errors from upstream transport errors?**
They represent different failures. Parse errors mean the payload shape is bad. Transport errors mean the call was unstable or too slow.

**How would you swap Gemini for another provider later?**
Keep app code calling `ask(prompt)` and change only the client implementation inside the wrapper boundary.

**What metrics would you log in production?**
At minimum: request ID, provider, model, latency, retry count, timeout count, and parse-failure count.
