# 13-Day Revision Quiz — 40 Interview Questions
## Based on ACTUAL code and concepts from Days 1-13

---

## SECTION 1: Python Fundamentals (Days 1-4) — 10 Questions

### Q1. What does `from google import genai` do and why do we need `load_dotenv()` before it?

<details>
<summary>Answer</summary>
`from google import genai` imports the Google Generative AI SDK. `load_dotenv()` loads environment variables from a `.env` file into `os.environ` so the API key is available without hardcoding it. Pattern: `client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))`.
</details>

### Q2. What are the 5 basic data types in Python? Give one example from the day2 code.

<details>
<summary>Answer</summary>
- `str`: `name = 'krishna'`
- `int`: `years_experience = 3`
- `bool`: `is_employed = True`
- `float`: `current_salary = 100000.0`
- `NoneType`: absence of value

Day2 code used `type()` to verify each variable's type.
</details>

### Q3. What is the difference between `*args` and `**kwargs`? Show with day4 examples.

<details>
<summary>Answer</summary>
`*args` collects positional arguments into a tuple: `def sum_all(*numbers)` — can call `sum_all(1,2,3)`.
`**kwargs` collects keyword arguments into a dict: `def introduce(**info)` — can call `introduce(name="krishna", role="engineer")`.
Both allow flexible function signatures.
</details>

### Q4. What is a set in Python and when would you use it instead of a list?

<details>
<summary>Answer</summary>
A set is an unordered collection of unique elements. Use it when you need:
- Deduplication: `set([1,1,2])` → `{1, 2}`
- Set operations: `skills_python & skills_gcp` (intersection) or `skills_python | skills_gcp` (union)
Day4 code used sets to find overlapping skills between Python and GCP skill sets.
</details>

### Q5. What does list comprehension do? Convert this loop to a comprehension: `result = [] for x in range(10): result.append(x*2)`

<details>
<summary>Answer</summary>
List comprehension creates a list in one line: `result = [x*2 for x in range(10)]`.
It is faster and more readable for simple transformations. Day4 also covered dict comprehension: `{k: v for k, v in items if v > 0}`.
</details>

### Q6. What is `__init__` and what does `self` mean in a Python class?

<details>
<summary>Answer</summary>
`__init__` is the constructor — it runs automatically when you create an object: `doc = Document(title, content)`.
`self` refers to the current instance, giving each object its own data. Day4/Day6 covered this: `self.title = title` stores the title on that specific instance.
</details>

### Q7. What is the difference between a class method and a static method?

<details>
<summary>Answer</summary>
- Class method (`@classmethod`): receives `cls` as first arg, can modify class state. Called as `ClassName.method()` or `instance.method()`.
- Static method (`@staticmethod`): receives no implicit first arg, acts like a regular function inside a class namespace.
Day4 notes: class methods are for alternative constructors, static methods for utility functions.
</details>

### Q8. What is the difference between `==` and `is` in Python?

<details>
<summary>Answer</summary>
`==` compares VALUES: `[1,2] == [1,2]` is True.
`is` compares IDENTITY (same object in memory): `[1,2] is [1,2]` is False (two different list objects).
Use `is` for `None` checks: `if x is None`.
</details>

### Q9. Explain the difference between `def func(a, b=10)` and `def func(*args)`. When would you pick each?

<details>
<summary>Answer</summary>
`def func(a, b=10)`: Fixed signature with optional param. Best when you know the exact params.
`def func(*args)`: Variable-length positional args. Best when the number of inputs is unknown.
Pick the first for clarity; pick the second for flexibility (like a sum function that takes any number of values).
</details>

### Q10. What does `f"Name: {name}"` do and what is it called?

<details>
<summary>Answer</summary>
It is an f-string (formatted string literal, Python 3.6+). It evaluates expressions inside `{}` at runtime. Day2 used: `f"Name: {name}, City: {city}"`. Faster and more readable than `%s` or `.format()`.
</details>

---

## SECTION 2: Data Handling + OOP (Days 5-7) — 10 Questions

### Q11. How do you read and write JSON files in Python? Show the day5 pattern.

<details>
<summary>Answer</summary>
```python
import json
# Read
with open("config.json") as f:
    data = json.load(f)
# Write
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```
Day5 used this pattern for `config.json` and `config_mini.json` handling.
</details>

### Q12. What is the difference between `json.load()` and `json.loads()`?

<details>
<summary>Answer</summary>
- `json.load(file_object)`: reads from a FILE object.
- `json.loads(string)`: reads from a STRING. The 's' stands for string.
Similarly, `json.dump(obj, file)` writes to file, `json.dumps(obj)` returns a string.
</details>

### Q13. What does `with open("file.txt") as f:` guarantee?

<details>
<summary>Answer</summary>
The `with` statement (context manager) guarantees the file is CLOSED after the block, even if an exception occurs. Without it, you must call `f.close()` manually and risk leaving files open on errors.
</details>

### Q14. What is the `os` module used for? Give 3 examples from day5.

<details>
<summary>Answer</summary>
The `os` module provides operating system interfaces:
1. `os.getenv("KEY")` — read environment variables
2. `os.path.exists("file.txt")` — check if file exists
3. `os.listdir(".")` — list directory contents
Day5 used `os` for cross-platform file path handling and env var access.
</details>

### Q15. What are the 4 pillars of OOP? Which did Day6 focus on?

<details>
<summary>Answer</summary>
1. **Encapsulation** — bundling data + methods inside a class
2. **Inheritance** — child class reuses parent class code
3. **Polymorphism** — same interface, different behavior
4. **Abstraction** — hiding complexity, exposing essentials

Day6 focused on **Encapsulation** (classes, `__init__`, `self`, instance variables).
</details>

### Q16. What is inheritance in Python? Show a minimal example.

<details>
<summary>Answer</summary>
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof!"
```
`Dog` inherits from `Animal`. The child class can override or extend parent methods. Day6 exercises covered class hierarchies.
</details>

### Q17. What is `__str__` vs `__repr__` in a Python class?

<details>
<summary>Answer</summary>
- `__str__`: Human-readable, used by `print(obj)`. Example: `"Document(title='resume')"`
- `__repr__`: Developer-readable, used by `repr(obj)` and debugger. Example: `"Document('resume', '...')"`
Rule: `__repr__` should be unambiguous, `__str__` should be readable.
</details>

### Q18. What is an HTTP GET vs POST request? When would you use each?

<details>
<summary>Answer</summary>
- **GET**: Retrieve data. Parameters go in URL query string. Idempotent (safe to repeat).
- **POST**: Send data to create/update. Data goes in request body. Not idempotent.
Day7 REST API exercises used `requests.get(url)` for fetching and `requests.post(url, json=data)` for creating.
</details>

### Q19. What does `response.json()` do after `requests.get()`?

<details>
<summary>Answer</summary>
It parses the response body as JSON and returns a Python dict/list. Equivalent to `json.loads(response.text)`.
Day7 pattern: `r = requests.get("https://api.example.com/data"); data = r.json()`.
</details>

### Q20. What is a REST API and what does REST stand for?

<details>
<summary>Answer</summary>
REST = REpresentational State Transfer. A REST API uses HTTP methods (GET, POST, PUT, DELETE) on resources identified by URLs. Key constraints: stateless, uniform interface, client-server separation. Day7 covered calling REST APIs with the `requests` library.
</details>

---

## SECTION 3: GCP Fundamentals (Days 8-10) — 10 Questions

### Q21. What is the difference between a GCP Region and a Zone?

<details>
<summary>Answer</summary>
- **Region**: Geographic area (e.g., `us-central1`, `asia-south1`). Contains multiple zones.
- **Zone**: Specific data center within a region (e.g., `us-central1-a`). Deploys individual resources.
Choose regions close to your users for lower latency. Choose zones for high availability.
</details>

### Q22. What is Cloud Run and why is it good for ML/AI services?

<details>
<summary>Answer</summary>
Cloud Run is a serverless container platform. You give it a container image, it handles scaling, networking, and infrastructure.
Good for ML/AI because:
- Auto-scales to zero when no requests (cost savings)
- Scales up for burst traffic
- Runs any language/framework via containers
Day8/Day10 deployed FastAPI+Gemini on Cloud Run.
</details>

### Q23. What is the difference between Cloud Run and Cloud Functions?

<details>
<summary>Answer</summary>
- **Cloud Functions**: Event-driven, single-function, limited runtimes (Node.js, Python, Go). Max timeout 60 min.
- **Cloud Run**: Container-based, any runtime, any language, full application. Max timeout 60 min.
For production AI services, Cloud Run is preferred because you control the full environment.
</details>

### Q24. What is IAM and what does "least privilege" mean?

<details>
<summary>Answer</summary>
IAM = Identity and Access Management. Controls WHO can do WHAT on WHICH resources.
Least privilege = give only the minimum permissions needed. Example: if a service only reads BigQuery, give it `roles/bigquery.dataViewer`, NOT `roles/owner`.
Day9 covered IAM roles, service accounts, and WIF (Workload Identity Federation).
</details>

### Q25. What is a Service Account in GCP?

<details>
<summary>Answer</summary>
A service account is a special account for applications (not humans). It has an email like `my-app@project.iam.gserviceaccount.com`. Applications use it to authenticate API calls. Best practice: create one per service, grant minimal roles.
</details>

### Q26. What is a GCS Bucket and how is it different from a file system?

<details>
<summary>Answer</summary>
- **Bucket**: Flat container for objects (files). Globally unique name. No true folders — just object name prefixes.
- **File system**: Hierarchical directories.
GCS is object storage, not block storage. Objects are immutable — you overwrite, not edit in place.
Day10 covered bucket creation and object operations.
</details>

### Q27. What is the `gcloud` CLI and give 3 commands you used.

<details>
<summary>Answer</summary>
`gcloud` is the command-line tool for GCP operations:
1. `gcloud config set project MY_PROJECT` — set active project
2. `gcloud run deploy --source .` — deploy to Cloud Run
3. `gcloud auth application-default login` — authenticate for local dev
Day8-Day10 used `gcloud` for deployment and configuration.
</details>

### Q28. What is WIF (Workload Identity Federation)?

<details>
<summary>Answer</summary>
WIF lets external workloads (GitHub Actions, AWS, on-prem) access GCP WITHOUT service account keys. Instead of downloading a JSON key file (security risk), you configure a trust relationship. Day9 covered WIF as the modern, secure way to authenticate external systems to GCP.
</details>

### Q29. What does `uvicorn` do and why do we need it for FastAPI?

<details>
<summary>Answer</summary>
FastAPI is a framework — it defines routes and logic. Uvicorn is the ASGI server that actually listens for HTTP requests and passes them to FastAPI. Without uvicorn, FastAPI has no way to receive network traffic.
Pattern: `uvicorn main:app --host 0.0.0.0 --port 8080`
Day10 used uvicorn in the Dockerfile CMD.
</details>

### Q30. What is a Dockerfile and why does Cloud Run need one?

<details>
<summary>Answer</summary>
A Dockerfile defines how to build a container image: base OS, install dependencies, copy code, start command. Cloud Run runs containers, so it needs an image built from a Dockerfile.
Day10 pattern:
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```
</details>

---

## SECTION 4: FastAPI + Production Patterns (Days 10-13) — 10 Questions

### Q31. What is Pydantic and why does FastAPI use it?

<details>
<summary>Answer</summary>
Pydantic is a data validation library. FastAPI uses it to:
1. Define request/response schemas as Python classes
2. Auto-validate incoming data (type, length, range)
3. Auto-generate OpenAPI docs
4. Return 422 errors for invalid data

Day12 pattern: `class EchoRequest(BaseModel): message: str = Field(..., min_length=1, max_length=200)`
</details>

### Q32. What is the difference between Pydantic V1 and V2 syntax? Give 2 changes.

<details>
<summary>Answer</summary>
1. Validator: V1 uses `@validator` → V2 uses `@field_validator` with `@classmethod`
2. Serialization: V1 `.dict()` → V2 `.model_dump()`
3. Parsing: V1 `.parse_obj()` → V2 `.model_validate()`
Day12-Day13 strictly uses V2 syntax per project rules.
</details>

### Q33. What is a 422 error and when does FastAPI return it?

<details>
<summary>Answer</summary>
422 Unprocessable Entity — FastAPI returns this when request data fails Pydantic validation. Examples:
- Missing required field
- String too short/long (violates `min_length`/`max_length`)
- Wrong data type (string where int expected)

This happens BEFORE your handler code runs. Day12 proved this with intentional field name mismatches.
</details>

### Q34. What is `Field(...)` in Pydantic and what does `...` mean?

<details>
<summary>Answer</summary>
`Field(...)` defines validation rules for a field. The `...` means the field is REQUIRED (no default value).
Examples:
- `Field(..., min_length=1)` — required, at least 1 character
- `Field(default=10, ge=1, le=100)` — optional, between 1-100
Day12/Day13 used Field constraints on all request models.
</details>

### Q35. How do you add a custom exception handler in FastAPI?

<details>
<summary>Answer</summary>
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_failed", "details": sanitized_errors}
    )
```
Day13 added a custom handler that sanitizes Pydantic error objects before returning JSON.
</details>

### Q36. What was the JSON serialization bug in Day 13 and how was it fixed?

<details>
<summary>Answer</summary>
**Bug**: `TypeError: Object of type ValueError is not JSON serializable`
**Cause**: `exc.errors()` from Pydantic returns dicts with raw Python objects (like `ValueError` instances) in `ctx` sub-dicts.
**Fix**: Created a `_sanitize()` function that extracts only JSON-safe fields (`type`, `loc`, `msg`) and discards the `ctx` sub-dict.
**Lesson**: Never pass raw exception objects to JSONResponse — always sanitize first.
</details>

### Q37. What is the request lifecycle in FastAPI? (middleware → route → validation → handler → response)

<details>
<summary>Answer</summary>
1. **ASGI Server** (uvicorn) receives HTTP request
2. **Middleware** processes request (logging, CORS, timing)
3. **Router** matches URL path to endpoint function
4. **Pydantic** validates request body/query params (422 if invalid)
5. **Handler** runs business logic
6. **Response** serialized to JSON and returned

Day12 mapped this lifecycle explicitly; Day13 added error handling at step 4.
</details>

### Q38. What is `httpx` and why is it used in FastAPI tests?

<details>
<summary>Answer</summary>
`httpx` is an HTTP client library (like `requests` but async-capable). FastAPI's `TestClient` uses httpx under the hood to make requests to your app without starting a real server.
Day12/Day13 pattern:
```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/health")
assert response.status_code == 200
```
</details>

### Q39. What is the difference between `BaseModel.model_dump()` and `dict()` in Pydantic?

<details>
<summary>Answer</summary>
- `model_dump()`: Pydantic V2 method. Returns a dict of the model's data. Supports `exclude_none`, `exclude_unset`, etc.
- `dict()`: Pydantic V1 method. DEPRECATED in V2 — raises warning.
Always use `model_dump()` in new code. Day13 used it for serializing validated data.
</details>

### Q40. Explain fail-fast validation. Why is it important for AI/ML services?

<details>
<summary>Answer</summary>
Fail-fast = reject bad input as early as possible, before it reaches expensive business logic.
For AI/ML services, this is critical because:
- LLM calls cost money per token — don't waste them on invalid requests
- Validation is cheap (microseconds); LLM calls are expensive (seconds + dollars)
- Clear error messages help frontend developers fix issues faster

Day13's custom exception handler implements fail-fast: every invalid request gets a clean 422 before the handler runs.
</details>

---

## SCORING GUIDE

| Score | Level | Action |
|-------|-------|--------|
| 36-40 | Interview Ready | You can explain any Day 1-13 topic confidently |
| 28-35 | Strong Foundation | Review the questions you missed, re-read that day's notes |
| 20-27 | Needs Review | Spend 1-2 days re-doing the exercises for weak sections |
| Below 20 | Restart | Go back to the day folders and build from scratch |

---

## HOW TO USE THIS QUIZ

1. **Solo drill**: Read question, speak the answer out loud, then check.
2. **Mock interview**: Have someone ask you random questions from this list.
3. **Spaced repetition**: Mark questions you got wrong, revisit in 2 days.
4. **Speed round**: Try answering all 40 in under 20 minutes.

---

*Generated from actual repo content (Days 1-13) | Revision Date: April 2026*
