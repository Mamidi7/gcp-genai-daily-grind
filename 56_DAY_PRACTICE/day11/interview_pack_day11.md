# Interview Pack - Day 11 (Config Reliability)

## Problem Context
Service works on one machine but fails in another environment due to hidden config assumptions.

## Data Flow (Input -> Process -> Output)
Input:
- Env vars (`GCP_PROJECT_ID`, `GCP_LOCATION`, optional credentials path)
- JSON config file

Process:
1. Load env
2. Load JSON object
3. Validate required env keys
4. Build safe summary for diagnostics

Output:
- Valid/invalid status
- Safe summary (no raw secrets)

## Failure Mode and Recovery
Failure:
- Required env var missing.

Recovery:
- Set env var in `.env` or deployment config.
- Re-run validation check.

## 30-Second Answer
I improved backend reliability by separating config from code, loading env and JSON explicitly, and adding fail-fast validation for required keys. This prevents late runtime failures and makes deployment safer.

## 90-Second STAR
Situation:
Our app had config assumptions hardcoded and failed unpredictably across environments.
Task:
Make config handling safe, portable, and interview-grade.
Action:
I introduced a clear env contract, JSON config loader, required-key validation, and safe summary output that masks sensitive paths.
Result:
Configuration errors are detected early, debugging became faster, and deployment reliability improved.

## 3-Minute Technical Walkthrough
I use a three-part strategy. First, env vars handle environment-specific values. Second, JSON handles non-secret structured runtime config. Third, validation enforces required keys and fails fast with clear messages. For observability, I return a safe summary with masked paths and key lists instead of secrets. This prevents leakage while still giving enough debug visibility. The result is consistent behavior from local to Cloud Run and fewer production surprises.

## Follow-up Questions
1. Why not keep everything only in env vars?
2. Which keys should be mandatory vs optional?
3. How would you handle secrets in Cloud Run?
4. What happens if JSON config is malformed?
5. How do you test missing env paths in CI?
