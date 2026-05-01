# REVISION GUIDE — Days 1-14 (Python Fundamentals → BigQuery + FastAPI)

**Purpose**: One read-through before interviews. Covers fundamentals to first production service.

---

## DAY 1 — Python + Gemini API (First Contact)

### What You Built
First script calling Gemini API using `google.genai` SDK.

```python
from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain RAG in one sentence"
)
```

### Core Concepts
1. **SDK vs raw HTTP**: SDK wraps auth, retries, serialization. Raw HTTP (Day 7) gives control.
2. **Environment variables**: Never hardcode API keys. Use `.env` + `load_dotenv()`.
3. **Model naming**: `gemini-2.0-flash` = fast/cheap. `gemini-2.0-flash-001` = stable version.

### Interview 30s
"I started by building a simple Python client for Gemini using the official SDK, loading credentials from environment variables. This taught me the basic request-response flow before adding any framework complexity."

### Common Mistake
Hardcoding API keys in source code. Fix: `os.getenv("GEMINI_API_KEY")` with `.env` file.

### Quick Check
- Can you write the 4-line Gemini call from memory?
- Why should API keys never be in git?

---

## DAY 2 — Variables, Types, f-strings

### What You Built
Variable declarations with type awareness and f-string formatting.

```python
name = "Krishna"
years_experience = 3
is_employed = True
print(f"Name: {name}, Years: {years_experience}")
```

### Core Concepts
1. **Dynamic typing**: Python figures out type at runtime. `type()` confirms it.
2. **f-strings**: `f"{var}"` is the modern way. Faster and more readable than `.format()`.
3. **Boolean in conditions**: `if is_employed:` not `if is_employed == True:`.

### Interview 30s
"Python variables are dynamically typed. I use f-strings for readable output and always validate types when data crosses system boundaries."

### Common Mistake
Using `+` for string concatenation with numbers. Fix: f-strings handle type conversion naturally.

---

## DAY 3 — Functions, *args, **kwargs

### What You Built
Reusable functions with flexible argument patterns.

### Core Concepts
1. **`*args`**: Collects extra positional args into a tuple.
2. **`**kwargs`**: Collects extra keyword args into a dict.
3. **Default parameters**: `def f(x=10)`. Defaults evaluate once — mutable defaults (lists) are dangerous.
4. **RAG connection**: `chunk_text()` is a function that splits documents — the FIRST step in any RAG pipeline.

### Interview 30s
"I write functions with clear signatures, using *args and **kwargs for flexibility. I understand that mutable default arguments are a Python trap — never use `def f(x=[])` in production."

### Common Mistake
```python
def add_item(item, items=[]):  # WRONG — same list every call
    items.append(item)
    return items
```
Fix: `def add_item(item, items=None):` then `if items is None: items = []`.

### Quick Check
- What type is `*args`? What type is `**kwargs`?
- Why is `def f(x=[])` dangerous?

---

## DAY 4 — Classes + OOP

### What You Built
A `Document` class with serialization methods — the foundation for RAG document handling.

```python
class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata else {}

    def to_dict(self):
        return {"title": self.title, "content": self.content}

    @classmethod
    def from_json(cls, json_data):
        return cls(title=json_data.get("title"), content=json_data.get("content"))
```

### Core Concepts
1. **`__init__`**: Constructor. Runs when you create an instance.
2. **`self`**: Refers to the current instance. Always first param of instance methods.
3. **`@classmethod`**: Alternative constructor. Receives `cls` (the class), not `self`.
4. **`to_dict()`**: Converts object to dictionary for JSON serialization.
5. **OOP in RAG**: `Document` stores chunks. `DocumentProcessor` manages collections. Later: inherit for PDFDocument, TextDocument.

### Interview 30s
"I built a Document class for RAG pipelines with proper initialization, JSON serialization, and class methods for alternative construction. This pattern scales to collections and specialized document types."

### Common Mistake
Forgetting `self.` when accessing attributes inside methods. Fix: Always use `self.attribute`.

### Quick Check
- When do you use `@classmethod` vs regular method?
- Can you write a Document class with `to_dict()` and `from_json()`?

---

## DAY 5 — JSON, File I/O, os module

### What You Built
Reading/writing files and JSON — config persistence and result logging.

```python
import json

# Write
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read
with open("data.json", "r") as f:
    data = json.load(f)
```

### Core Concepts
1. **`with` statement**: Guarantees file closes even if error occurs.
2. **`json.dump` vs `dumps`**: `dump` writes to file, `dumps` returns string.
3. **`os` module**: `os.path.exists()`, `os.listdir()`, `os.makedirs()` for filesystem ops.
4. **SQL Track**: Window functions — `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`.

### Interview 30s
"I use Python's json module for config files and evaluation results. Combined with file I/O and the os module, this is how I persist data in RAG pipelines and ML workflows."

### Common Mistake
Using `json.dumps` when you meant `json.dump`, or forgetting `indent=2` for readable output.

### Quick Check
- What's the difference between `json.dump()` and `json.dumps()`?
- Why use `with open(...)` instead of `f = open(...)`?

---

## DAY 6 — pip, venv, Packages

### What You Built
Understanding Python environment isolation and package management.

### Core Concepts
1. **`python -m venv venv`**: Create isolated environment.
2. **`source venv/bin/activate`**: Activate it.
3. **`pip install -r requirements.txt`**: Install dependencies.
4. **`pip freeze > requirements.txt`**: Pin exact versions.
5. **Why isolate**: Different projects need different package versions. Global installs = conflicts.

### Interview 30s
"I manage Python dependencies with virtual environments and pinned requirements.txt files. This ensures reproducible builds across local, CI, and production deployments."

### Common Mistake
Installing packages globally instead of in venv. Fix: Always activate venv first.

---

## DAY 7 — REST APIs with requests

### What You Built
Calling Gemini API using raw HTTP (requests library) — no SDK.

```python
import requests

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
data = {
    "contents": [{"parts": [{"text": "Your prompt"}]}]
}
response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
result = response.json()
```

### Core Concepts
1. **GET vs POST**: GET fetches, POST creates/sends data.
2. **Headers**: `Authorization: Bearer <token>` or API key in query param.
3. **`response.raise_for_status()`**: Automatically raises on 4xx/5xx.
4. **`response.json()`**: Parses JSON response. Can fail if response isn't JSON.
5. **Timeout**: Always set `timeout=30` on requests to prevent hanging.

### Interview 30s
"I can call REST APIs both with SDKs and raw HTTP using the requests library. I understand GET vs POST, handle authentication headers, validate status codes, and always set timeouts to prevent hanging connections."

### Common Mistake
Not checking status_code before calling `.json()`. Fix: `response.raise_for_status()` first.

### Quick Check
- What's the difference between GET and POST?
- Why should you always set a timeout on requests?

---

## DAY 8 — GCP + Cloud Run Deployment

### What You Built
First cloud deployment understanding — GCP projects, regions, zones, Cloud Run.

### Core Concepts
1. **Project**: Container for ALL GCP resources. Has unique global ID.
2. **Region**: Geographic area (us-central1, asia-south1).
3. **Zone**: Specific data center within a region.
4. **Cloud Run**: Serverless container platform. Auto-scales 0→1000+. Pay per use.
5. **Deployment flow**: `gcloud auth login` → set project → enable API → `gcloud run deploy --source .`

### Interview 30s
"I deployed services to Cloud Run, GCP's serverless container platform. It auto-scales from zero and I only pay for what I use. I understand the hierarchy: Organization → Project → Region → Zone."

### Common Mistake
Deploying to the wrong project or region. Fix: `gcloud config set project PROJECT_ID` and specify `--region`.

---

## DAY 9 — GCP Console + IAM

### What You Built
Understanding GCP access control — primitive and predefined roles.

### Core Concepts
1. **Primitive Roles**:
   - **Viewer**: Read-only everywhere.
   - **Editor**: Read + write + delete. CANNOT manage IAM.
   - **Owner**: Full control + IAM management + billing.
2. **Predefined Roles**: Granular. `roles/bigquery.dataViewer`, `roles/storage.objectAdmin`.
3. **Custom Roles**: Combine specific permissions. Use when predefined doesn't fit.
4. **Principle of Least Privilege**: Give minimum access needed. Never use Owner in production.

### Interview 30s
"In GCP, I use predefined roles following least privilege. Viewer is read-only, Editor can modify resources but cannot manage IAM, and Owner has full control. For production, I prefer granular predefined roles like BigQuery Data Viewer over primitive roles."

### Common Mistake
Giving Editor role for IAM management tasks. Fix: Only Owner can add/remove users.

### Quick Check
- What's the difference between Editor and Owner?
- Why are predefined roles better than primitive roles in production?

---

## DAY 10 — Cloud Storage + FastAPI Gemini Service

### What You Built
A production-style FastAPI app integrated with Gemini, deployed to Cloud Run.

### Core Concepts
1. **GCS Storage Classes**:
   - **Standard**: Frequently accessed. Hot data.
   - **Nearline**: 30-day minimum. Backup, monthly access. (Think "N-30")
   - **Coldline**: 90-day minimum. Quarterly access. (Think "C-90")
   - **Archive**: 365-day minimum. Yearly access. (Think "A-365")
2. **Bucket**: Global unique name. Container for objects.
3. **Object**: Files up to 5TB. Identified by name (includes path).
4. **FastAPI + Gemini**: Pydantic validation, retry logic, middleware, error handling.

### Key Architecture
```
Client Request
    |
    v
FastAPI Router → Pydantic Validation → Handler → Gemini API Call
    |
    v
JSON Response (with request_id, retries_used)
```

### Interview 30s
"I built a FastAPI service that calls Gemini with Pydantic validation, retry logic, and structured error responses. It's deployed on Cloud Run. For storage, I use GCS with the right storage class — Standard for hot data, Nearline for backups, Coldline for archives."

### Common Mistake
Choosing wrong storage class and paying early deletion fees. Fix: Match access pattern to class.

### Quick Check
- What's the retention mnemonic for GCS classes?
- Can you name 3 features of your Day 10 FastAPI app?

---

## DAY 11 — Config Reliability (.env + JSON + Validation)

### What You Built
Fail-fast configuration handling — env vars + JSON config + validation.

### Core Concepts
1. **`.env`**: Environment-specific secrets and values. Never commit to git.
2. **JSON config**: Non-secret structured config (profiles, limits, toggles).
3. **Fail-fast**: Validate required env vars at startup. Crash early with clear messages.
4. **Safe summary**: Log only key names and safe values. Mask secrets.

### Interview 30s
"I separate configuration from code, load env and JSON explicitly, and fail fast on missing required keys. This prevents late runtime failures and makes deployment safer across environments."

### Common Mistake
Hardcoding project IDs. Fix: `os.getenv("GCP_PROJECT_ID")` with validation.

---

## DAY 12 — FastAPI Basics (/health + /echo + Validation)

### What You Built
First FastAPI app with health check and echo endpoint. Proved request lifecycle.

### Request Lifecycle
```
Client → FastAPI Router → Pydantic Validation → Handler → JSON Response
                          |
                    fails → 422 (before handler)
```

### Core Concepts
1. **`@app.get("/health")`**: Liveness probe. Returns `{"status": "ok"}`.
2. **`@app.post("/echo")`**: Accepts body, validates with Pydantic, returns response.
3. **Pydantic BaseModel**: Defines expected shape. `Field(..., min_length=1)` adds constraints.
4. **422 vs 500**: 422 = validation failed (before handler). 500 = handler crashed.

### Interview 30s
"I built a FastAPI service with `/health` and `/echo` to understand the request lifecycle. FastAPI routes the request, Pydantic validates input, and the handler runs only if validation passes. I tested both valid and invalid requests to prove 422 happens before business logic."

### Common Mistake
Thinking 500 means bad input. Fix: 422 = input problem. 500 = code problem.

### Quick Check
- What's the difference between 422 and 500?
- Why is `/health` important in production?

---

## DAY 13 — FastAPI Errors + Custom Validation

### What You Built
Strict input constraints with custom exception handler and clean error responses.

### Core Concepts
1. **`@field_validator`**: Custom validation logic beyond Field constraints. (Pydantic V2 syntax)
2. **`RequestValidationError`**: Raised when Pydantic validation fails.
3. **Custom exception handler**: Catches validation errors and returns consistent JSON shape.
4. **Sanitization**: `exc.errors()` may contain non-JSON objects. Must sanitize before JSONResponse.
5. **Fail-fast**: Reject bad input early. Handler never sees invalid data.

### Interview 30s
"I extended FastAPI with strict Pydantic Field validators and a custom exception handler so every validation failure returns the same clean error structure. I also added business-level HTTPException for reserved keywords. The goal is fail-fast validation — reject bad input early with clear messages."

### Common Mistake
Passing `exc.errors()` directly to JSONResponse. Fix: Sanitize non-JSON objects first.

### Quick Check
- Can you write a `@field_validator` that checks minimum stripped length?
- Why sanitize error objects before JSONResponse?

---

## DAY 14 — BigQuery SQL Patterns

### What You Built
Five real SQL patterns on public Stack Overflow data + debug journal for join cardinality.

### Core Concepts
1. **Aggregation**: `COUNT`, `AVG`, `SUM` with `GROUP BY`. Trend discovery.
2. **CTE + Join**: `WITH cte AS (...) SELECT ... FROM cte JOIN ...`. Readable complex queries.
3. **Window Functions**: `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`. Ranking without collapsing rows.
4. **Subquery**: Nested SELECT for outlier scoring and filtering.
5. **VECTOR_SEARCH schema**: Preparing BigQuery tables for embedding-based retrieval.
6. **Join cardinality**: Bad joins return believable but wrong results. Always check with `COUNT(DISTINCT ...)`.

### BigQuery in AI Systems
```
App logs / docs / embeddings
            |
            v
        BigQuery
   raw → transformed → analytics
            |
            v
   retrieval prep / offline eval / debugging
```

### Interview 30s
"I built five BigQuery SQL patterns on public data: aggregation, CTE joins, window functions, subqueries, and vector search schema design. I also debugged a duplicate-row issue caused by incorrect join cardinality. BigQuery serves both analytics and retrieval foundations in my AI systems."

### Common Mistake
Assuming joins are correct because they don't crash. Fix: Cardinality checks with `COUNT(DISTINCT)`.

### Quick Check
- What's the difference between ROW_NUMBER and RANK?
- Why do bad joins not crash loudly?

---

## CROSS-DAY CONNECTIONS (Interview Gold)

```
Day 1-2 (Python basics)
    ↓
Day 3-4 (Functions + Classes)
    ↓  Document class, chunk_text(), to_dict/from_json
Day 5 (JSON + File I/O)
    ↓  Config persistence, result logging
Day 6 (venv + pip)
    ↓  Reproducible environments
Day 7 (REST APIs)
    ↓  Raw HTTP understanding before SDK abstraction
Day 8-9 (GCP + IAM)
    ↓  Deployment and security foundation
Day 10 (GCS + FastAPI Gemini)
    ↓  First production service
Day 11 (Config reliability)
    ↓  Safe deployment
Day 12-13 (FastAPI validation)
    ↓  Fail-fast input handling
Day 14 (BigQuery)
    ↓  Data layer for analytics and retrieval
Day 15+ (RAG, embeddings, eval)
    ↓  AI-specific layers on top
```

---

## RETENTION TEST (Do This Now)

Write these 4 snippets from memory. No peeking.

**Snippet 1: Safe env var loading**
```python
def get_project_id() -> str:
    """Load GCP project ID from env. Raise if missing."""
    # 3 lines max
```

**Snippet 2: Document class with JSON serialization**
```python
class Document:
    def __init__(self, title: str, content: str):
        # 3 lines

    def to_dict(self) -> dict:
        # 1 line

    @classmethod
    def from_json(cls, data: dict):
        # 1 line
```

**Snippet 3: FastAPI health + echo**
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)

# Add /health GET endpoint
# Add /echo POST endpoint
```

**Snippet 4: BigQuery CTE + window function**
```sql
-- Find top 3 posts per tag by score
WITH ranked AS (
    SELECT
        title,
        tag,
        score,
        _______ OVER (PARTITION BY tag ORDER BY score DESC) as rn
    FROM posts
)
SELECT * FROM ranked WHERE rn <= 3;
```

**Time limit**: 15 minutes total.

**Pass criteria**: All 4 compile/run correctly.

If you pass → Day 15 revision or forward progress.
If stuck → we debug together.

---

## INTERVIEW PACK QUICK REFERENCE

| Day | 30s Pitch | Key Number / Mnemonic |
|-----|-----------|----------------------|
| 1 | First Gemini API call with SDK | `gemini-2.0-flash` |
| 2 | Variables, types, f-strings | `type()` to inspect |
| 3 | Functions, *args, **kwargs | Mutable defaults trap |
| 4 | Document class with JSON serialization | `to_dict()` / `from_json()` |
| 5 | JSON read/write, file I/O | `with open(...)` guarantees close |
| 6 | pip, venv, requirements.txt | `pip freeze > requirements.txt` |
| 7 | REST APIs with requests | Always set `timeout=` |
| 8 | Cloud Run deployment | Auto-scales 0 → 1000+ |
| 9 | IAM: Viewer / Editor / Owner | Editor CANNOT manage IAM |
| 10 | GCS + FastAPI Gemini | N-30, C-90, A-365 |
| 11 | Config reliability | Fail fast on missing env |
| 12 | FastAPI basics | 422 = validation, 500 = code |
| 13 | Custom validation + error handler | Sanitize before JSONResponse |
| 14 | BigQuery SQL patterns | Check join cardinality |

---

## GAPS TO CLOSE

Based on repo audit, these days need strengthening:

- **Day 1-2**: Very light. Add one small exercise file each.
- **Day 6**: Notes are thin. Add venv activation commands.
- **Day 8**: WIF_NOTES.md exists but may need cleanup.
- **Day 10**: FastAPI app is solid but needs real model integration confirmed.

---

*Generated from local repo + GitHub audit. Last updated: 2026-05-01*
