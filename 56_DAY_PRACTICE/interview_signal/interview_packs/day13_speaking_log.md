# Day 13 Interview Pack — FastAPI Errors & Validation

## Topic
FastAPI input validation, custom exception handlers, business rule enforcement

---

## 30-Second Answer (Final Version)
> "I built a three-layer validation system for a FastAPI service — Pydantic Field validators for input constraints, a custom exception handler for clean error shapes, and an HTTPException for business rules. The key insight is fail-fast: reject bad input before it reaches any business logic, and always return consistent error structures so clients can handle failures programmatically."

---

## 90-Second STAR

**Situation**: Production API was returning raw Pydantic 422 responses with non-serializable objects, causing TypeError in exception handler.

**Task**: Add strict input constraints, normalize all error responses, and enforce business rules at the API layer.

**Action**:
1. Added Pydantic Field validators with min/max length and a custom @field_validator
2. Built a custom RequestValidationError handler with a `_sanitize()` function that strips non-JSON-serializable objects from error dicts
3. Added HTTPException for reserved keywords ("ignore" case-insensitive)
4. Removed restrictive return type annotation that was causing ResponseValidationError

**Result**: 13/13 tests pass. All three failure modes (blank input, oversized input, reserved keyword) return clean, consistent JSON. No more serialization crashes in the error path.

---

## Debug → Interview Story

| Bug | Root Cause | Interview Angle |
|-----|-----------|----------------|
| `TypeError: Object of type ValueError is not JSON serializable` | Pydantic embeds raw Python objects in `ctx` field of error dicts | "I never assume library error objects are JSON-safe" |
| `ResponseValidationError: 'clean_char_count' must be a string` | Return type hint `-> dict[str, str]` triggered response validation for mixed types | "Type hints in FastAPI aren't documentation — they enforce constraints" |
| `"IGNORE this"` not caught | Case-sensitive `startswith("ignore")` | "Business rules should be case-insensitive unless case is semantically meaningful" |

---

## Speaking Improvement Notes (getfluently.app feedback)

**What went well**:
- Clear three-layer structure
- Specific test case numbers (13/13 passing)
- Technical precision on the root cause

**What to improve**:
- Lead with business impact, not the code structure
- Use concrete scale: "10K requests/day" not "high traffic"
- Pause between each validation layer so interviewer can follow

**Next mock interview reminders**:
1. Impact statement first ("Reduced API errors by catching bad input before business logic")
2. Use specific numbers
3. Ask clarifying question before diving deep
