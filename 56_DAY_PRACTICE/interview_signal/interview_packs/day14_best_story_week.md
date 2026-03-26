# Best Interview Story — Week of March 21–26

## The Pick: Day 13 — FastAPI Exception Handler Bug

This is the strongest debug-to-interview conversion from the week. Three real bugs, all fully documented, all with production implications.

---

## 30-Second Answer (Final)

> "I built a three-layer validation system for a FastAPI service — Pydantic Field validators for input constraints, a custom exception handler for clean error shapes, and an HTTPException for business rules. The key insight is fail-fast: reject bad input before it reaches business logic, and always return consistent error structures so clients can handle failures programmatically."

---

## 90-Second STAR

**Situation:**
A FastAPI endpoint was crashing with `TypeError: Object of type ValueError is not JSON serializable` whenever a blank request body was sent.

**Task:**
Add strict input validation, normalize all error responses to clean JSON, and enforce a business rule (reject questions starting with "ignore") — without breaking the existing happy path.

**Action:**
1. Added Pydantic `Field()` constraints and a `@field_validator` for custom stripped-length check
2. Built a custom `RequestValidationError` handler with a `_sanitize()` function that extracts only `type`, `loc`, `msg` from each error dict — discarding the raw Python objects in `ctx`
3. Added `HTTPException` for the reserved keyword check, returning a clean `400 {"error": "reserved_keyword", ...}`
4. Discovered and fixed a `ResponseValidationError` caused by a wrong return type annotation `-> dict[str, str]` that enforced string values on an integer field

**Result:**
13/13 tests pass. All three failure modes produce clean, consistent JSON. The handler never receives malformed data. The bug is prevented by a regression test that validates the error structure itself.

---

## 3-Minute Technical Walkthrough

**Input → Validation → Error Handling → Response**

```
POST /question {"question": ""}
        ↓
Pydantic QuestionRequest model
        ↓
Field validator: min_length=1, max_length=500
@field_validator: stripped value must be >= 3 chars
        ↓
FAIL → RequestValidationError raised
        ↓
Custom handler catches it
        ↓
_sanitize() strips non-JSON fields from exc.errors()
        ↓
JSONResponse {"error": "validation_failed", "message": "...", "fields": [...]}
        ↓ HTTP 422
```

**The two gotchas:**

1. `exc.errors()` is NOT JSON-safe — Pydantic embeds `ValueError` instances in `ctx`
2. Return type hints `-> dict[str, str]` trigger RESPONSE validation, not documentation

---

## Five Interview Q&As

**Q1: What is fail-fast validation?**
A: Rejecting bad input at the validation layer, before any business logic runs. The sooner you fail, the less damage bad data can do.

**Q2: Why a custom exception handler?**
A: Default FastAPI 422 responses are raw and inconsistent. A custom handler standardizes the shape so clients always get the same fields.

**Q3: 400 vs 422 — what's the difference?**
A: 422 = Pydantic rejected the input (validation failure). 400 = input passed validation but violates a business rule.

**Q4: Why sanitize exc.errors()?**
A: Pydantic embeds raw Python objects (like `ValueError` instances) in the `ctx` field. These crash `json.dumps()`. Always extract only the safe string fields.

**Q5: How does @field_validator work in Pydantic V2?**
A: Decorator on a classmethod. Receives the raw value, can transform it or raise `ValueError`. If it returns a value, that becomes the field's value. If it raises, Pydantic treats it as a validation failure.

---

## Speaking Notes (getfluently.app)

**What worked:**
- Clear three-layer structure
- Specific test count (13/13)
- Root cause precision

**What to improve:**
- Lead with business impact ("Reduced API errors by catching bad input before business logic")
- Use concrete scale
- Pause between each validation layer
