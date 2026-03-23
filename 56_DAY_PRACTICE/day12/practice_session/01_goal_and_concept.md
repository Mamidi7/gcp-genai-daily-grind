# Goal And Concept

## Why Today Matters
This is your first API basics day.
Later GenAI apps also need the same flow: request -> validation -> handler -> response.

## What We Are Building
One FastAPI app with:
- `GET /health`
- `POST /echo`

## Plain English Concept
- Client sends request to API.
- FastAPI checks which route matches.
- If body is needed, Pydantic validates it.
- If input is correct, handler runs.
- Response comes back as JSON.

## ASCII Flow
```text
Client
  |
  v
FastAPI route
  |
  v
Validation
  |
  +---- fail -> 422 error
  |
  v
Handler
  |
  v
JSON response
```

## What To Understand Before Running
- `/health` is for checking service is alive.
- `/echo` is for checking request and response flow.
- Invalid input test is important because interviews ask about failure paths too.
