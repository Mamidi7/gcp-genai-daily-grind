# Day 15 Debug Journal — Wrapper Parse Failure

## Symptom
Wrapper raised parse error when model output was not valid JSON.

## Root Cause
Directly trusting upstream text is unsafe; model output can contain plain text, markdown, or partial JSON.

## Fix
- Parse with `json.loads`.
- Enforce required keys: `answer`, `confidence`, `source`.
- Validate confidence range `[0, 1]`.
- Raise explicit `ParseError` for malformed payloads.

## Prevention
- Keep output schema strict.
- Add parse-failure tests in wrapper smoke checks.
- Keep retry logic separate from parse logic.

## Interview Impact
I can explain that reliability starts at interface boundaries: transport retries and schema validation solve different failure modes.
