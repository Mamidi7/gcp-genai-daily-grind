# Day 11 - Files, JSON, Environment Variables

## One-Line Goal
Build backend confidence by handling config safely using `.env` + JSON and fail-fast validation.

## Why Day 11 Matters
Today is not about fancy AI features. Today is about reliability.
If config handling is weak, production breaks even when model code is correct.

## Today's Syllabus
1. What goes in `.env` and why
2. How to load JSON config safely
3. How to avoid printing secrets
4. Missing env var failure path
5. Interview explanation: why hardcoding is risky

## Session Plan (90 Minutes)
1. Concept warmup (10 min)
2. Build mini config flow (30 min)
3. Add fail-fast validation (15 min)
4. Debug one failure path (10 min)
5. Interview conversion (15 min)
6. Wrap up + notes (10 min)

## Deliverables (Non-Negotiable)
- One code artifact
- One debug artifact
- One interview artifact (30s, 90s STAR, 3-min)
- One short day note

## Files in This Folder
- `notes.md` - concepts in simple language
- `exercises.py` - hands-on tasks (fill TODOs)
- `solution.py` - reference implementation
- `debug_journal_day11.md` - symptom -> root cause -> fix -> prevention
- `interview_pack_day11.md` - interview-ready answers
- `day11_checklist.md` - execution tracker
- `config/runtime_profile.json` - sample JSON config
- `.env.example` - sample env contract

## Run Commands
```bash
cd /Users/krishnavardhan/projects/GCP_GENAI/gcp-genai-daily-grind/56_DAY_PRACTICE/day11
python3 exercises.py
python3 solution.py
```

## Common Mistakes to Avoid
- Hardcoding project IDs in source code
- Printing full credential paths in logs
- Assuming env vars exist without validation
- Mixing secrets inside JSON files committed to git

## End State
You should be able to clearly explain:
- what goes in,
- what happens inside,
- what comes out,
- what can fail,
- how you verify.
