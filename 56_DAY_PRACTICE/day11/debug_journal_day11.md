# Day 11 Debug Journal

## Symptom
`config validation failed: GCP_PROJECT_ID missing`

## Root Cause
Environment variable not set in current shell/runtime.

## Fix
Set `GCP_PROJECT_ID` in `.env` or deployment environment.

## Prevention
- Keep `.env.example` updated.
- Run validation check before startup/deploy.
- Add CI check for required env keys.

## Impact
- failure prevented: app now fails fast instead of failing later in model calls
- correctness improved: env contract is explicit
- debug time saved: missing config is identified immediately

## Interview Translation
### 30s
I added fail-fast validation for required environment config, so deployment issues are caught before runtime traffic hits the service.

### 90s STAR
Situation: Config errors were discovered late during requests.
Task: Catch config issues early and safely.
Action: Added required env validation and safe config summary.
Result: Faster diagnosis, reduced runtime failures, cleaner deployment flow.

### 3-min Deep Dive
I separated config concerns into three layers: env, JSON, and validation. I then made validation explicit for required keys like `GCP_PROJECT_ID`. Finally, I exposed safe diagnostics that never print raw secrets. This design gives predictable behavior across local, CI, and Cloud Run.
