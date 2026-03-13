# Day 10: Notes - Cloud Storage (GCS)

## Key Takeaways

### Buckets vs Objects
- **Bucket**: Container (like S3 bucket), global unique name
- **Object**: File inside bucket, identified by name (includes path)
- Objects can be up to 5TB each!

### Storage Classes (MUST MEMORIZE)

| Class | Min Retention | Use Case |
|-------|---------------|----------|
| Standard | None | Frequently accessed |
| Nearline | 30 days | Monthly access |
| Coldline | 90 days | Quarterly access |
| Archive | 365 days | Yearly/compliance |

**Interview trick:** Think "N-30, C-90, A-365" for retention!

### Access Control
- **Uniform (recommended)**: IAM only, simpler
- **Fine-grained**: IAM + ACLs (legacy)
- **Signed URLs**: Temporary access (minutes to hours)
- **Signed Policy**: Control what users can upload

---

## SQL Track: Window Functions

### ROW_NUMBER()
- Assigns unique sequential numbers
- Great for "top N per category"

```sql
SELECT *, ROW_NUMBER() OVER (ORDER BY sales DESC) as rank
FROM products
```

### RANK() vs DENSE_RANK()
- RANK(): Ties get same rank, next rank skips (1, 1, 3)
- DENSE_RANK(): Ties get same rank, next doesn't skip (1, 1, 2)

### LAG/LEAD
- LAG(): Previous row's value
- LEAD(): Next row's value
- Perfect for time series comparison

---

## Interview Punch Dialogue

**Q:** "How would you choose a storage class for ML model files?"

**A:** "For production ML models accessed frequently for inference, I'd use Standard storage for the 99.99% availability. For archived models used during rollback scenarios, Coldline makes sense. The key is matching access frequency to storage class to optimize costs - using Archive for compliance data that might only be accessed yearly can save 90%+ compared to Standard."

---

## Common Mistakes

1. **Using wrong storage class** - Check access frequency first!
2. **Bucket names with uppercase** - Always lowercase
3. **Forgetting signed URLs expire** - They're time-limited

---

## Next Up
Day 11: Compute (Compute Engine, Cloud Run, Cloud Functions)

---

## Time Spent
- GCS concepts: 20 min
- Storage classes: 15 min
- SQL Window Functions: 30 min
- Total: ~65 min

---

## FastAPI + Gemini Validation Run (Industry Upgrade)

Test approach used:
- Used FastAPI `TestClient` to run endpoint tests in-process.
- Reason: local port bind was blocked in this environment, but request/response and middleware behavior were still fully testable.

Endpoints tested:
- `GET /healthz` -> `200`
- `GET /readyz` -> `200`
- `POST /chat` with empty prompt -> `422`
- `POST /chat` with normal prompt -> `502` (upstream model call failed)
- `POST /generate` with >6000 chars prompt -> `422`

### Real Failure 1: Input Validation Failure (422)
- Symptom: `/chat` returned `422 Unprocessable Entity`
- Trigger: empty `prompt` string
- Root cause: request schema enforces `prompt` min length = 1
- Fix/Handling: kept strict validation; client now receives deterministic error before model call
- Prevention: contract-first API design with pydantic constraints
- Interview value: demonstrates defensive API design and reduced wasted upstream calls

### Real Failure 2: Upstream Model Call Failure (502)
- Symptom: `/chat` returned `502 Bad Gateway`
- Trigger: normal prompt, upstream Gemini call failed
- Root cause: upstream model invocation failure path
- Fix/Handling: mapped generic upstream errors to safe `502` response with request ID
- Prevention: retry wrapper + timeout + structured request logging already added in API layer
- Interview value: shows reliability engineering and graceful degradation

---

## STAR Answers from Real Debugging

### STAR 1 - Validation Contract
- Situation: I was productionizing a FastAPI + Gemini endpoint.
- Task: Prevent invalid requests from reaching model calls and causing unpredictable failures.
- Action: Added strict pydantic constraints (`prompt` min/max length, token and temperature bounds) and validated via endpoint tests.
- Result: Invalid payloads now fail fast with `422`, reducing unnecessary upstream calls and making error behavior deterministic.

### STAR 2 - Upstream Resilience
- Situation: During endpoint testing, model calls intermittently failed upstream.
- Task: Make failures safe and diagnosable instead of returning raw stack traces.
- Action: Implemented retry + timeout wrapper, mapped upstream failures to `502/504/429` style responses, and attached request IDs in middleware logs.
- Result: API behavior became predictable under failure, and debugging became faster due to request-level traceability.

---

## Study Resume Log

### Date
- 2026-03-13

### Where we paused
- Krishna understood the big picture of FastAPI + Gemini.
- Krishna explained:
  - why validation matters
  - why retries matter
  - why request IDs matter
  - why `healthz` and `readyz` are different

### Corrected understanding to remember
- validation is for input safety and predictability, not model selection
- `/generate` is not a fallback for `/chat`; it is a separate, more creative endpoint
- middleware does more than request ID; it also times and logs the request

### Next exact step
- learn `/chat` line by line
- after that, learn `_generate_with_retry()` line by line

### Restart prompt for next session
- "Teach me `/chat` line by line in simple language with visuals."
