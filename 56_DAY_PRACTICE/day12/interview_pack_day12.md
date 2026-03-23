# Interview Pack - Day12

## 30-second Answer
"I built a small FastAPI service with `/health` and `/echo` to understand the request lifecycle clearly. FastAPI first routes the request, Pydantic validates the input, the handler runs only if validation passes, and then FastAPI returns JSON. I tested both a valid and invalid request, so I can explain why `422` happens before business logic."

## 90-second STAR
- Situation: Before moving deeper into Applied AI systems, I wanted a clear foundation on API request handling.
- Task: Build a small service that proves health checks, JSON body validation, and predictable error behavior.
- Action: I created a FastAPI app with `/health` and `/echo`, added a Pydantic body model, tested one valid payload and one invalid payload, then forced a handler bug to practice debugging.
- Result: I can now explain `request -> validation -> handler -> response` confidently, and I can connect the same pattern to the FastAPI service I already deployed on Cloud Run.

## 3-minute Walkthrough
1. The client sends a request to either `/health` or `/echo`.
2. FastAPI matches the method and path to the correct endpoint function.
3. For `/echo`, Pydantic checks the body before the handler runs.
4. If the JSON contains `message`, the handler reads `payload.message` and returns `{"echo": ...}`.
5. FastAPI serializes that Python dictionary into JSON and returns `200`.
6. If the JSON body is missing `message`, FastAPI returns `422` before entering the handler.
7. If the input is valid but the handler uses the wrong field like `payload.text`, the request reaches the handler and fails with `500`.
8. That distinction matters in interviews because it shows I understand validation errors versus application logic bugs.

## Common Interview Questions
1. What is FastAPI request validation?
Answer: It is the step where FastAPI and Pydantic check the request shape and types before your handler logic runs.

2. Why do we test invalid input?
Answer: Invalid input testing proves the API fails early and predictably instead of letting bad data reach business logic.

3. What is the difference between `422` and `500` here?
Answer: `422` means the request body was invalid. `500` means the body passed validation but the handler code failed.

4. Why keep `/health` in production services?
Answer: It gives a quick liveness signal so humans and platforms can check whether the app process is responding.

5. How does this connect to Applied AI work?
Answer: AI endpoints still start with the same backend flow. Model calls, retries, and GCP deployment sit after correct request validation and handler design.
