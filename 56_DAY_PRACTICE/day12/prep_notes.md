# DAY12 - FastAPI Basics Closeout

## WHY TODAY MATTERS
This day makes your request flow explanation strong before you touch bigger Applied AI topics.
Interviewers expect you to explain how invalid input fails before business logic or model calls.

## WHAT WE'RE BUILDING TODAY
`main.py` and `test_main.py` for a small FastAPI service with `/health` and `/echo`.

## TIME BUDGET
| Block | Time | What you do |
|---|---|---|
| Concept | 15 min | Read the flow once and redraw the ASCII diagram |
| Build | 30 min | Type or review `main.py` manually |
| Verify | 25 min | Run `/health`, valid `/echo`, invalid `/echo` |
| Break it | 15 min | Trigger the forced failure and observe the error |
| Debug | 15 min | Fill `debug_journal_day12.md` and `api_evidence.txt` |
| GCP step | 10 min | Inspect the Day10 Cloud Run service in the console |
| Interview | 10 min | Speak the 30-second and 90-second answers aloud |
| Total | ~2 hours | Close the day without guessing |

## CONCEPT IN PLAIN ENGLISH
FastAPI receives the request and matches it to the correct endpoint.
Pydantic checks the body before your handler runs.
If validation passes, your function runs and returns Python data.
FastAPI converts that data into JSON and sends the status code.
If validation fails, FastAPI sends `422` without entering your business logic.

## ASCII DIAGRAM
```text
Client
  |
  | GET /health
  v
FastAPI router ---> health() ------------------> {"status":"ok"}

Client
  |
  | POST /echo {"message":"hello"}
  v
FastAPI router -> Pydantic body check -> echo() -> {"echo":"hello"}

Client
  |
  | POST /echo {}
  v
FastAPI router -> Pydantic body check fails -> 422 validation response
```

## THE CODE
Copy this into `main.py` if you want to type it manually from scratch.

```python
# day12_fastapi_basics.py | python>=3.12 | requires: fastapi[standard]==0.135.1 pydantic==2.7.1 uvicorn[standard]==0.29.0
"""
Day 12 manual practice app.
Run:
    python3 -m uvicorn main:app --host 127.0.0.1 --port 8012
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Day12 FastAPI Basics", version="1.0.0")


class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}
```

Optional verification file is `test_main.py`.

## HOW TO RUN IT
Terminal 1:

```bash
cd /Users/krishnavardhan/projects/GCP_GENAI/gcp-genai-daily-grind/56_DAY_PRACTICE/day12
python3 -m uvicorn main:app --host 127.0.0.1 --port 8012
```

Expected startup log:
```text
Uvicorn running on http://127.0.0.1:8012
```

Terminal 2:

```bash
curl -i http://127.0.0.1:8012/health
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{"message":"hello fastapi"}'
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{}'
python3 -m unittest test_main.py -v
```

Expected output highlights:
- `/health` -> `HTTP/1.1 200 OK` and `{"status":"ok"}`
- valid `/echo` -> `HTTP/1.1 200 OK` and `{"echo":"hello fastapi"}`
- invalid `/echo` -> `HTTP/1.1 422 Unprocessable Entity`
- unit test run -> 3 tests pass

Paste the real outputs into `api_evidence.txt`.

## FORCED FAILURE
Change `payload.message` to `payload.text` inside `echo()`, then rerun the valid `/echo` request.

Expected error:
- client side: `500 Internal Server Error`
- server log: `AttributeError: 'EchoRequest' object has no attribute 'text'`

Why it breaks:
The request body is valid, but the handler is reading a field that does not exist on the Pydantic model.

## DEBUG CARD
```text
Symptom:
Root cause:
Fix:
Prevention:
```

## GCP CONSOLE ACTION
1. Open GCP Console -> Cloud Run.
2. Open your Day10 FastAPI Gemini service in `us-central1`.
3. Check the `Revisions` tab and confirm which revision has live traffic.
4. Open the service URL and compare deployed `/readyz` with your local `/health`.
5. Check `Logs` once so you can connect local API practice to production request traces.

Why this matters:
Today you are learning the small local flow that later becomes production health and readiness checks in Cloud Run.

## INTERVIEW OUTPUT
30-second answer:
"I built a small FastAPI service with `/health` and `/echo` so I could clearly explain the request lifecycle. A request first hits the FastAPI router, then Pydantic validates the body, then the handler runs, and finally FastAPI returns JSON. I tested one valid request and one invalid request, which showed me why `422` happens before business logic."

90-second STAR skeleton:
- Situation: I wanted a clean way to understand FastAPI request handling before moving deeper into AI backends.
- Task: Build a small service that proves health checks, request body validation, and predictable error handling.
- Action: I created `/health`, added `/echo` with a Pydantic body model, ran valid and invalid requests, and forced one handler bug to practice debugging.
- Result: I can now explain `request -> validation -> handler -> response` clearly and connect that same pattern to larger GCP services.

3-minute walkthrough:
1. The client sends either `GET /health` or `POST /echo`.
2. FastAPI matches the method and path to the correct handler.
3. For `/echo`, Pydantic checks whether the JSON body contains `message`.
4. If validation passes, the handler reads `payload.message` and returns a Python dictionary.
5. FastAPI converts that dictionary into JSON and sends `200`.
6. If the body is `{}`, validation fails first and FastAPI returns `422`.
7. If the body is valid but my code uses a wrong field like `payload.text`, then validation passes and the handler fails with `500`.
8. That difference helps in interviews because I can explain validation bugs separately from handler bugs.
