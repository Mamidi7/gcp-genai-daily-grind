# Debug Journal - Day13

## Required Case 1 — JSON Serialization Failure in Exception Handler

- Symptom: `POST /question` with blank body caused `TypeError: Object of type ValueError is not JSON serializable`
- Root cause: `exc.errors()` returns Pydantic error dicts that contain raw Python objects like `ValueError` instances inside `ctx` sub-dicts. Passing these directly to `JSONResponse` causes `json.dumps()` to fail.
- Fix: Created `_sanitize()` function that extracts only the JSON-safe fields (`type`, `loc`, `msg`) from each error dict, discarding `ctx` and other non-serializable objects.
- Prevention: Never pass Pydantic error objects directly to JSON. Always extract safe string fields. Add a test for the error structure itself (`test_422_has_clean_error_structure`).
- Impact: Custom exception handlers must be serialization-safe. This is a common FastAPI gotcha.

---

## Required Case 2 — Response Model Type Mismatch

- Symptom: Valid POST /question returned `ResponseValidationError: 'clean_char_count' must be a string`
- Root cause: Return type annotation `-> dict[str, str]` told FastAPI to validate that ALL dict values are strings. `clean_char_count` is an integer, not a string. FastAPI tried to serialize the response through Pydantic and failed.
- Fix: Removed the restrictive return type annotation. FastAPI now infers the correct types from the actual returned values.
- Prevention: When returning arbitrary dicts with mixed types, omit the `-> dict[str, str]` annotation or use a Pydantic response model. Be precise with return type hints.
- Impact: Return type hints in FastAPI aren't just documentation — they trigger response validation. Wrong hints = silent runtime failures.

---

## Optional Case — Reserved Keyword Case Sensitivity

- Symptom: "ignore this" was caught but "IGNORE this" was not.
- Root cause: Business rule check used `payload.question.startswith("ignore")` — case-sensitive.
- Fix: Changed to `payload.question.lower().startswith("ignore")` so it catches all case variants.
- Prevention: Business rules for string content should usually be case-insensitive unless case is semantically meaningful. Add a test for case-insensitive matching.
- Impact: Case-insensitive checks are more robust. Always ask: should this be case-sensitive?

---

## Your Actual Run Notes

- Command: `python3 -m pytest test_main.py -v`
- Output: 3 failed initially — 2 from bugs above, 1 from syntax typo in test name
- What I learned: Pydantic error objects aren't JSON-safe, and return type hints trigger response validation in FastAPI.
