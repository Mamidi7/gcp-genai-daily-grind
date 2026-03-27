# Day 15 Debug Journal — Wrapper Parse Failure and Gateway Boundaries

## Symptom
Wrapper raised parse error when model output was not valid JSON.

## Root Cause
Directly trusting upstream text is unsafe; model output can contain plain text, markdown, or partial JSON.

## Fix
- Parse with `json.loads`.
- Enforce required keys: `answer`, `confidence`, `source`.
- Validate confidence range `[0, 1]`.
- Raise explicit `ParseError` for malformed payloads.

## Transport vs Parse Failure
- Parse failure means the model responded, but the payload shape is wrong.
- Timeout or upstream failure means the model call itself was unstable or too slow.
- These should be handled differently because retrying malformed JSON blindly often does not solve the real problem.

## Prevention
- Keep output schema strict.
- Add parse-failure tests in wrapper smoke checks.
- Keep retry logic separate from parse logic.
- Log request metadata so bad outputs can be traced later.

## Interview Impact
I can explain that reliability starts at interface boundaries: transport retries and schema validation solve different failure modes.

## Why This Matters in Real Systems
If a team mixes parse logic, timeout logic, and business logic in one route handler, debugging becomes messy. A wrapper keeps those concerns in one place and makes incidents easier to diagnose.
