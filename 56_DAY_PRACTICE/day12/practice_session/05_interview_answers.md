# Interview Answers

## 30-Second Answer
I built a small FastAPI app with two endpoints: `/health` and `/echo`.
`/health` checks if the API is alive.
`/echo` returns the input message.
I also tested one invalid request and saw FastAPI validation error.

## 90-Second STAR
- Situation: I was preparing backend basics for AI engineer interviews.
- Task: Build a small API and understand request validation.
- Action: I created `/health`, created `/echo`, added a request body model, and tested valid and invalid payloads.
- Result: Valid request worked, and invalid request returned a clear `422` validation error.

## 3-Minute Walkthrough
1. I built a FastAPI app with `/health` and `/echo`.
2. Request comes in, FastAPI matches route, then validation happens.
3. If input is correct, handler runs and sends JSON response.
4. If `message` is missing, request fails before handler.
5. This matters because production APIs must handle both success and failure clearly.
