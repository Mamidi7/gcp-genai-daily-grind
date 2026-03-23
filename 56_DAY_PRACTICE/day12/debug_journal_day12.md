# Debug Journal - Day12

## Required Case - Forced Failure
- Symptom: Valid `POST /echo` returned `500 Internal Server Error`.
- Root cause: The handler tried to read `payload.text` even though the Pydantic model only defines `message`.
- Fix: Change the code back to `payload.message`.
- Prevention: Keep handler field names aligned with the request model and keep one passing `/echo` test in `test_main.py`.
- Impact: This proves that validation and handler logic are different failure stages.

## Your Actual Run Notes
- Command:
- Output:
- What I learned:

## Optional Case
- Symptom:
- Root cause:
- Fix:
- Prevention:
- Impact:
