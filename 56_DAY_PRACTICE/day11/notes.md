# Day 11 Notes - Simple and Interview-Focused

## 1) Restate Goal
Config ni safe ga handle cheyyadam: `.env` + JSON + fail-fast checks.

## 2) Concept in 3-6 Lines
- `.env` is for environment-specific values (project id, region, flags).
- JSON file is useful for non-secret structured config (profile, limits, toggles).
- Never hardcode env-specific values in source code.
- Validate required env vars at startup or via health endpoint.
- Show only safe summary in logs/API (mask paths/secrets).

## 3) Minimal Flow (Input -> Process -> Output)
Input:
- `GCP_PROJECT_ID`, `GCP_LOCATION` from env
- `runtime_profile.json` from file

Process:
1. Read env values
2. Read JSON values
3. Validate required env vars
4. Return safe summary

Output:
- Config summary + validation status

## 4) Common Mistake + Fix
Mistake:
- `PROJECT_ID = "my-dev-project"` hardcoded in code.

Fix:
- `PROJECT_ID = os.getenv("GCP_PROJECT_ID")`
- If missing, return clear error (`503` / startup fail).

## 5) Check Question
Why is hardcoded config dangerous when moving from local to Cloud Run?

## 6) Tiny Exercise
Write one function `validate_required_env()` that checks only `GCP_PROJECT_ID` and returns a clear error list.

## Interview Line (Use Directly)
"I separate configuration from code, load env and JSON explicitly, and fail fast on missing required keys so deployment failures are caught early."
