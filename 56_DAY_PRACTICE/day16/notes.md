# Day 16 Notes

## What I built today
- Structured output pipeline: Gemini JSON mode → extract_json() → json.loads → Pydantic validation
- Retry wrapper that feeds parse errors back into the LLM prompt
- 3 real schemas: SentimentResult, EntityExtraction, ToolCall (agent routing)
- Parse failure gallery: 6 common failure modes with correct handling

## Key concepts learned
1. **Two validation gates**: json.loads for syntax, Pydantic for semantics
2. **extract_json()**: Must handle markdown fences, preamble text, trailing garbage
3. **Retry with context**: Don't just retry — tell the LLM exactly what went wrong
4. **Monitor retry rate**: If avg attempts > 1.5, fix the prompt, don't add more retries

## Error I hit
- Mock responses returning plain text instead of JSON (simulated real Gemini behavior)
- Pydantic rejecting `"confidence": 1.5` even though JSON was valid — this is the semantic layer working correctly

## Root cause
- LLMs are text generators first — JSON is not their native format
- Schema constraints in prompts are "suggestions" to the model, not guarantees

## Fix applied
- Force JSON mode at API level (response_mime_type)
- Post-process with extract_json() for belt-and-suspenders reliability
- Pydantic as the hard gate — if it fails, it fails, retry with the error

## Prevention added
- Every LLM call goes through structured_llm_call(), never raw text
- Metadata tracking (attempts, errors) for monitoring

## 90-second interview version
"In my AI pipeline, LLM outputs were randomly breaking downstream code. I built a 3-layer structured output handler: regex extraction for messy text, JSON parsing for syntax, and Pydantic validation for schema correctness. On failure, I feed the exact error back into a retry. This dropped parse failures from 15% to under 1%, and the retry rate itself became a prompt quality metric."

## How this connects to the sprint
- Day 16 = structured output foundation
- Day 17 = embeddings (next layer in the RAG stack)
- Day 19-20 = eval harness uses these same Pydantic models for test case validation
- Day 31+ = agent tool calls will use ToolCall schema for routing
