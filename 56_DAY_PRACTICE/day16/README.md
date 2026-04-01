# Day 16 — Structured Output with Gemini (JSON Mode + Pydantic)

## Objective
Build a production-style LLM response parser that guarantees valid JSON output from Gemini using both JSON mode and Pydantic validation. This is the foundation for all tool use and agent routing.

## Why This Matters
- **#1 failure in LLM apps**: unpredictable output format
- Every agent system, every tool call, every eval — they ALL need structured output
- Anthropic and OpenAI both list "structured output" in their SDK as core skill
- Interview question: "How do you guarantee an LLM returns valid JSON?"

## What You'll Build
1. A Gemini caller that forces JSON mode
2. Pydantic models for response validation
3. A retry wrapper that re-prompts on parse failure
4. Debug journal: common parse failures and fixes

## Architecture (ASCII)
```
User Prompt
    │
    ▼
┌──────────────┐
│ Gemini API   │ ← response_mime_type="application/json"
│ (JSON Mode)  │
└──────┬───────┘
       │ raw JSON string
       ▼
┌──────────────┐
│ json.loads() │ ← first parse gate
└──────┬───────┘
       │ dict
       ▼
┌──────────────┐
│ Pydantic     │ ← second validation gate
│ Model.validate│
└──────┬───────┘
       │ typed object
       ▼
  Your App Code ✓
  
If ANY step fails → retry with error feedback
```

## Files
- `solution.py` — Full working implementation
- `exercises.py` — Practice challenges
- `notes.md` — Debug journal and interview prep
- `debug_journal_day16.md` — Error artifacts
- `interview_pack_day16.md` — STAR answers

## Prerequisites
- Google Cloud project with Vertex AI API enabled
- `google-cloud-aiplatform` and `pydantic` installed
- Set `GOOGLE_CLOUD_PROJECT` env var

## Interview Conversion
- **30s**: "I built a structured output layer that uses Gemini's JSON mode plus Pydantic validation with retry, guaranteeing parseable responses for downstream agent routing."
- **90s STAR**: "At my production project, LLM outputs were breaking our pipeline randomly. I added JSON mode enforcement at the API level, then wrapped it with Pydantic schema validation. When parsing failed, I fed the error back into a retry with the schema description. Parse failure rate dropped from ~15% to <1%. The key insight: don't trust LLM output — validate it like any external API."
