# Interview Pack - Config Safety with .env + JSON

## Problem Context

A backend service had mixed config handling: some values from env, some defaulted inline, and no explicit validation. This creates production risk and harder debugging.

## Data Flow (Input -> Process -> Output)

Input:
- `.env` variables
- `config/runtime_profile.json`

Process:
1. Load env using `python-dotenv`.
2. Load runtime JSON into a dictionary.
3. Build safe config summary (masked path, no secrets).
4. Validate required env vars (`GCP_PROJECT_ID`).

Output:
- `/config-summary` for safe diagnostics.
- `/config-validate` for fail-fast configuration checks.

## Failure Mode and Recovery

Failure:
`GCP_PROJECT_ID` missing.

Recovery:
Set variable in `.env`, restart service, rerun `/config-validate`.

Prevention:
Keep `.env.example` up to date and run validation endpoint before release/deploy.

## 30-Second Answer

I externalized config using `.env` and JSON, added safe diagnostics, and fail-fast validation. This prevents hardcoded secrets and catches environment errors before runtime failures.

## 90-Second STAR

Situation:
My FastAPI app had weak config hygiene and no validation guardrail.
Task:
Make config secure, portable, and interview-grade.
Action:
I added `.env` loading, JSON runtime config parsing, a redacted summary endpoint, and explicit validation for required env vars, then covered these with tests.
Result:
The app now fails early on misconfiguration and provides safe, actionable diagnostics without exposing secrets.

## 3-Minute Technical Walkthrough

I treat configuration as data, not code. At startup, the app loads `.env` values and a small JSON runtime profile. Instead of printing raw config, the summary endpoint returns a sanitized payload: model/project metadata, masked path, and JSON key list. A separate validation endpoint checks must-have values and returns `503` when incomplete. This split is important: one endpoint helps observability, the other enforces correctness. I added tests to verify both success and failure paths. In interviews, this demonstrates reliability thinking: clear contracts, safe diagnostics, and fail-fast behavior.

## Follow-up Questions I Should Expect

1. Why keep both `.env` and JSON instead of one source?
2. How would you handle secret management on Cloud Run?
3. What should be required vs optional env vars?
4. How would you prevent config drift across dev/stage/prod?
5. How would you handle a BigQuery timeout in your Python AI wrapper?
