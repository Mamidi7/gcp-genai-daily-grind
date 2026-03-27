# Day 15 Practice — LLM API Wrapper Design

This folder tracks Day 15 execution for a minimal, production-style wrapper.

## Goal
Build a simple Python wrapper that:
- accepts prompt text,
- returns a structured output shape,
- handles parse failures,
- includes retry + timeout placeholders.

## Files
- `DAY_PLAN.md` — execution checklist + evidence links
- `llm_api_wrapper.py` — minimal wrapper implementation
- `debug_journal_day15.md` — failure analysis (symptom -> root cause -> fix -> prevention)
- `interview_pack_day15.md` — 30s + 90s STAR + 3-min explanation

## Run
```bash
python3 llm_api_wrapper.py
```

## Validation
The script runs a local smoke test with a fake client and validates:
- success path parse,
- parse failure path,
- retry behavior.
