# Day 16 Debug Journal

## Error 1: LLM Returns Plain Text Instead of JSON

**Symptom:** `json.JSONDecodeError: Expecting value: line 1 column 1`
```
raw output: "The sentiment is positive with high confidence."
```

**Root Cause:** Gemini sometimes explains instead of returning JSON, especially with short or ambiguous prompts.

**Fix:** Two-layer approach:
1. Force `response_mime_type="application/json"` in Gemini API config
2. If that's not available, wrap prompt with: "You MUST respond with ONLY valid JSON, no other text."

**Prevention:** Always add schema description in the system prompt, not just the user prompt.

**Impact:** Parse failure rate dropped from ~15% to <1%.

---

## Error 2: Markdown Code Fences Wrapping JSON

**Symptom:** `json.JSONDecodeError: Expecting value: line 1 column 1`
```
raw output: '```json\n{"label": "positive", "confidence": 0.88}\n```'
```

**Root Cause:** LLMs trained on code often wrap JSON in markdown fences, even when asked not to.

**Fix:** `extract_json()` function that strips code fences with regex:
```python
re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
```

**Prevention:** Pre-process ALL LLM output through `extract_json()` before parsing.

---

## Error 3: Valid JSON But Wrong Schema Values

**Symptom:** `ValidationError: confidence: Input should be less than or equal to 1.0`
```
raw output: '{"label": "pos", "confidence": 1.5}'
```

**Root Cause:** LLM doesn't understand value constraints from prompt alone.

**Fix:** Use Pydantic Field constraints (`ge=0.0, le=1.0`) and retry with the exact error message:
```
"Your previous response failed: confidence must be ≤ 1.0. Try again."
```

**Prevention:** Include field constraints in the JSON schema passed to the model.

---

## Error 4: Empty Response on Timeout

**Symptom:** `StructedOutputError: No JSON content found in response`
```
raw output: ""
```

**Root Cause:** API timeout or rate limit returns empty string.

**Fix:** Check for empty response BEFORE attempting JSON parse. Raise early with clear message.

**Prevention:** Always have a timeout on the API call (e.g., 30 seconds) and treat empty as a retryable error.

---

## Key Takeaway (Interview Answer)

"LLM structured output has 3 failure modes: no JSON at all, broken JSON, and valid JSON but wrong schema. I handle each layer: extract JSON with regex, parse with json.loads, validate with Pydantic, and retry with the exact error as feedback. This dropped parse failures from 15% to under 1%."
