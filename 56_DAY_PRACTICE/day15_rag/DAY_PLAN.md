# DAY15_RAG - LLM API Wrapper Design

## Goal
Complete this day manually with verified outputs only.

## Syllabus
- Core concept understanding
- Small build artifact
- One debug artifact
- Interview conversion (30s, 90s STAR, 3-min)

## Step-by-Step Plan
1. Create minimal Python wrapper function
2. Define structured output shape
3. Handle parse failure path
4. Add retry/timeout placeholders
5. Prepare interview explanation: wrapper vs direct SDK

## Status Log (Update in this file)

| Block | Status | Start | End | Evidence |
|---|---|---|---|---|
| Step 1 | completed | 2026-03-27 | 2026-03-27 | `day15_rag/llm_api_wrapper.py` |
| Step 2 | completed | 2026-03-27 | 2026-03-27 | `WrapperResponse(answer, confidence, source)` |
| Step 3 | completed | 2026-03-27 | 2026-03-27 | `ParseError` path + `debug_journal_day15.md` |
| Step 4 | completed | 2026-03-27 | 2026-03-27 | timeout + retry logic in `SimpleLLMWrapper.ask` |
| Step 5 | completed | 2026-03-27 | 2026-03-27 | `interview_pack_day15.md` |
| Day Closeout | completed | 2026-03-27 | 2026-03-27 | README + code + debug + interview artifacts added |

## Completion Criteria
- [x] Code/query artifact done
- [x] Debug artifact done
- [x] Interview artifact done
- [x] Progress files updated (`SESSION_STATE.md`, `DAILY_PROGRESS_LOG.md`, `DAYWISE_EXECUTION_MEMORY.md`)


## Topic Completion Checkboxes

- [x] Step 1: Create minimal Python wrapper function
- [x] Step 2: Define structured output shape
- [x] Step 3: Handle parse failure path
- [x] Step 4: Add retry/timeout placeholders
- [x] Step 5: Prepare interview explanation: wrapper vs direct SDK
- [x] Day Closeout
