# Applied AI Day10 - Directive Completion

Date: 2026-03-21

## Python Function Flow (input -> inside -> output)

- `clean_question(text)`
  - input: raw text
  - inside: `strip()`, reject empty
  - output: clean string or `ValueError("question cannot be empty")`

- `make_payload(question, user_id)`
  - input: raw question + user id
  - inside: validate via `clean_question`
  - output: `{"user_id": ..., "question": ...}`

- `format_answer(answer, sources)`
  - input: answer text + source list
  - inside: trim answer
  - output: `{"answer": ..., "sources": [...]}`

- `build_request_log(question, status)`
  - input: question + status
  - inside: validate + length compute
  - output: `{"question": ..., "status": ..., "question_length": ...}`

## Invalid-Input Debug Artifact

- symptom: blank input crashed flow
- root cause: no early validation
- fix: fail-fast validation in `clean_question`
- prevention: always validate before payload/model call

## Manual Verification Snapshot

- `clean_question("  hello  ")` -> `hello`
- `build_request_log("  hi  ", "ok")` -> `{'question': 'hi', 'status': 'ok', 'question_length': 2}`
- `clean_question("")` -> `ValueError: question cannot be empty`
- `clean_question("   ")` -> `ValueError: question cannot be empty`
