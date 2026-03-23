# Interview Pack - Day13

## 30-second Answer

"I extended a FastAPI service with strict input constraints using Pydantic Field validators, then built a custom exception handler so every validation failure returns the same clean error structure. I also added a business-level HTTPException for reserved keywords. The goal is fail-fast validation — reject bad input early with clear messages, before it reaches any business logic."

## 90-second STAR

- Situation: APIs need to reject bad input early and return consistent error shapes — not raw Pydantic output.
- Task: Add input constraints, clean error responses, and a custom exception path to a FastAPI service.
- Action: Used Pydantic Field validators with min/max length, a @field_validator for custom logic, a custom RequestValidationError handler to normalize 422 responses, and an HTTPException for business rule violations.
- Result: All three failure paths now fail predictably — blank input returns 422, oversized returns 422, reserved keyword returns 400 — with consistent JSON shapes. The handler never sees bad data.

## 3-minute Walkthrough

1. The client sends a POST /question with a JSON body.
2. FastAPI matches the route and passes the body to the Pydantic QuestionRequest model.
3. Pydantic validates: question is required, must be 1-500 chars, and the @field_validator checks that stripped length >= 3.
4. If validation fails, FastAPI raises RequestValidationError BEFORE the handler runs.
5. My custom exception handler catches it and returns clean JSON: {"error": "validation_failed", "message": "...", "fields": [...]}
6. If validation passes, the handler runs. It checks if the question starts with "ignore". If so, raises HTTPException 400.
7. If both pass, returns the response with clean_char_count so the client knows the clean length.
8. The debug failure I reproduced: passing `exc.errors()` directly to JSONResponse caused a TypeError because Pydantic embeds raw Python ValueError objects. I fixed it with a `_sanitize()` function that extracts only JSON-safe fields.

## Common Interview Questions

1. What is fail-fast validation?
Answer: It means rejecting bad input as early as possible — at the validation layer, before any business logic runs. The sooner you fail, the less damage bad data can do.

2. Why use a custom exception handler?
Answer: The default FastAPI/Pydantic 422 response is raw and inconsistent. A custom handler standardizes the error shape so clients always get the same fields — error code, message, and field list.

3. What's the difference between 400 and 422?
Answer: 422 is for validation failures (Pydantic rejected the input). 400 is for business rule violations — the input passed validation but violates a rule the application cares about.

4. Why sanitize exc.errors() before JSON serialization?
Answer: Pydantic's error objects contain raw Python types like ValueError instances in the ctx field. These are not JSON-serializable. You must extract only the safe string fields before returning JSON.

5. How does @field_validator work in Pydantic V2?
Answer: It's a decorator on a classmethod. It receives the raw value, can transform it or raise ValueError. If it returns a value, that becomes the field's value. If it raises, Pydantic treats it as a validation failure.
