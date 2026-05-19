# Day 12 — FastAPI Interview Answers

## 30-Second Answer
"I built a FastAPI service by porting my Flask Cloud Run app line-by-line. The key difference: Pydantic validates POST body before the handler runs — returns 422 automatically instead of me writing manual checks in Flask. Same endpoints (/, /health, /info), but FastAPI gives auto-docs at /docs and doesn't need jsonify()."

## 90-Second STAR Answer

**Situation:** I had just deployed a Flask app to Cloud Run and wanted to learn FastAPI — it's the standard for AI backends.

**Task:** Port my Flask endpoints (/, /health, /info, /echo) to FastAPI and understand validation flows.

**Action:**
- Wrote same 4 endpoints in FastAPI with Pydantic models for POST input
- Tested valid request → 200, empty body → 422 (Pydantic auto-rejects before handler)
- Intentionally broke the handler (wrong field name) → 500 — proving validation and handler errors are separate layers
- Compared code side-by-side: Flask needs jsonify() + manual validation, FastAPI auto-converts dicts and auto-validates

**Result:** I can now explain FastAPI's request lifecycle clearly: route → validation → handler → response. Connected this to my production Day 10 FastAPI+Gemini app that uses the same patterns on Cloud Run.

## 3-Minute Technical Walkthrough

1. **App creation:** `FastAPI(title=...)` vs `Flask(__name__)` — FastAPI gets title/version in constructor
2. **Routes:** `@app.get()` / `@app.post()` — explicit method decorators. Flask uses one `@app.route()` with `methods=`
3. **JSON response:** FastAPI auto-converts dict → JSON. Flask needs `jsonify()`
4. **Input validation:** Pydantic `BaseModel` with `Field(min_length=1)` — validation happens in middleware BEFORE the handler. Flask requires manual `request.get_json()` + if/else checks
5. **Error codes:** Invalid body → 422 (structured error). Valid body + handler bug → 500. In Flask, both would be 500 or you'd hand-roll 400
6. **Running:** FastAPI needs uvicorn (ASGI server). Flask has built-in dev server
7. **Auto docs:** FastAPI serves Swagger at /docs and ReDoc at /redoc — zero config
