# Debug Journal — Exercise 1: Model Serving API

## Bug #1: Test assertion `latency_ms > 0` failed
```
ERROR: assert 0.0 > 0
CAUSE: Mocked model call returns instantly. time.perf_counter() difference rounds to 0.0ms.
FIX: Changed assertion to `latency_ms >= 0` — in real usage latency will always be positive.
IMPACT: Test was too strict for mocked environment.
PREVENTION: For timing assertions on mocked functions, use >= 0 not > 0.
```

## Bug #2 (Expected): Running tests without mocking calls real API
```
ERROR: If USE_REAL_MODEL=1 and tests don't mock call_model(), tests hit real Vertex AI.
CAUSE: Tests should ALWAYS mock external dependencies.
FIX: All tests use `patch("solution.model_api.call_model", new_callable=AsyncMock)`.
IMPACT: Without mocking, tests are slow, flaky, and cost money.
PREVENTION: Rule — never call real API in unit tests. Use integration test suite separately.
```

## Bug #3 (Expected): Pydantic V1 vs V2 confusion
```
ERROR: Using @validator instead of @field_validator
CAUSE: Old tutorials use Pydantic V1 syntax.
FIX: Use Pydantic V2: @field_validator, model_dump(), Field(...)
IMPACT: Code won't run with pydantic>=2.0
PREVENTION: Always check pydantic version. Use V2 syntax.
```
