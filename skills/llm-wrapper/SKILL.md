# skills/llm-wrapper/SKILL.md

## What this skill does
Provides `LLMWrapper` class — single source of truth for all Gemini calls in the project.
Handles: async generation, structured JSON output via Pydantic, latency logging, error handling.

## Location
`56_DAY_PRACTICE/2026-03-25_llm-wrapper/llm_wrapper.py`

## How to invoke
```python
from llm_wrapper import LLMWrapper
llm = LLMWrapper()
response = await llm.generate("your prompt")
parsed, meta = await llm.generate_structured("prompt", OutputSchema)
```

## Parameters
- `model_id`: str — defaults to `"gemini-2.0-flash-001"`
- `generate(prompt, system="", temperature=0.7, max_tokens=1024)` → `LLMResponse`
- `generate_structured(prompt, schema: BaseModel, system="", temperature=0.1)` → `tuple[BaseModel, LLMResponse]`

## Returns
- `LLMResponse.text`: str
- `LLMResponse.input_tokens`: int
- `LLMResponse.output_tokens`: int
- `LLMResponse.latency_ms`: float
- `LLMResponse.model`: str

## Dependencies
- `google-cloud-aiplatform>=1.57.0`
- `pydantic>=2.7.1`
- `vertexai` (part of google-cloud-aiplatform)

## Environment
- `GOOGLE_CLOUD_PROJECT` must be set
- `REGION=us-central1`, `MODEL=gemini-2.0-flash-001`

## Known issues
- Vertex AI SDK is synchronous — always wrap with `asyncio.to_thread()`
- Use `temperature=0.1` for structured output (reduces JSON formatting errors)
- Always `.strip()` the response text before parsing; Gemini sometimes wraps JSON in markdown fences

## Used by
- Day 13: Prompt registry → imports LLMWrapper
- Day 18: RAG Grounded → imports LLMWrapper
- Day 20: LLM-as-Judge → imports LLMWrapper
- Day 27: Constitutional AI → imports LLMWrapper
