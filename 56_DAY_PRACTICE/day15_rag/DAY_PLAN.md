# DAY15_RAG - LLM Gateway Wrapper Design

## Goal
Complete this day manually with verified outputs only.

## Syllabus
- Core concept understanding
- Small build artifact
- One debug artifact
- Interview conversion (30s, 90s STAR, 3-min)

## Industry Framing
This day is about building the gateway boundary between your app and any model provider.
The wrapper should own:
- request contract
- response contract
- structured output parsing
- timeout and retry policy
- basic request metadata for debugging

## ASCII Architecture
```text
API / App code
     |
     v
LLM Gateway Wrapper
  | parse JSON
  | validate schema
  | timeout / retry
  | attach request metadata
     |
     v
Provider SDK / Model
```

## Step-by-Step Plan
1. Create provider-agnostic wrapper interface
2. Define typed response shape with metadata
3. Handle parse/schema failure path
4. Separate timeout and upstream retry behavior
5. Prepare interview explanation: wrapper boundary vs direct SDK usage

## Status Log (Update in this file)

| Block | Status | Start | End | Evidence |
|---|---|---|---|---|
| Step 1 | completed | 2026-03-27 | 2026-03-27 | `day15_rag/llm_api_wrapper.py` |
| Step 2 | completed | 2026-03-27 | 2026-03-27 | `WrapperResponse(answer, confidence, source)` |
| Step 3 | completed | 2026-03-27 | 2026-03-27 | `ParseError` path + `debug_journal_day15.md` |
| Step 4 | completed | 2026-03-27 | 2026-03-27 | timeout + retry logic in `SimpleLLMWrapper.ask` |
| Step 5 | completed | 2026-03-27 | 2026-03-27 | `interview_pack_day15.md` |
| Day Closeout | completed | 2026-03-27 | 2026-03-27 | README + code + debug + interview artifacts added |

## Why This Matters in Real Systems
- Without a wrapper, every route or job re-implements SDK logic differently.
- Structured output validation stops bad model payloads from leaking deeper into the app.
- Timeout and retry policy belongs at the gateway boundary, not scattered across handlers.

## Completion Criteria
- [x] Code/query artifact done
- [x] Debug artifact done
- [x] Interview artifact done
- [x] Progress files updated (`SESSION_STATE.md`, `DAILY_PROGRESS_LOG.md`, `DAYWISE_EXECUTION_MEMORY.md`)


## Topic Completion Checkboxes

- [x] Step 1: Create provider-agnostic wrapper interface
- [x] Step 2: Define typed response shape with metadata
- [x] Step 3: Handle parse/schema failure path
- [x] Step 4: Separate timeout and upstream retry behavior
- [x] Step 5: Prepare interview explanation: wrapper boundary vs direct SDK usage
- [x] Day Closeout

## Practice Exercise
Explain how you would swap Gemini for another provider without changing API route code.

## Common Interview Questions
- Why not call the SDK directly from every route?
- Why separate parse errors from transport errors?
- What metrics should the wrapper emit in production?
