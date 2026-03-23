# Day12 API Contract Draft

## 1) GET /health
Purpose: quick service liveness check.

Request:
- Method: `GET`
- Path: `/health`
- Body: none

Success Response:
- Status: `200`
- Body:
```json
{"status":"ok"}
```

Failure Cases:
- Not expected in basic local setup unless server is down.

## 2) POST /echo
Purpose: return back the input message.

Request:
- Method: `POST`
- Path: `/echo`
- Body:
```json
{"message":"hello"}
```

Success Response:
- Status: `200`
- Body:
```json
{"echo":"hello"}
```

Validation Failure Cases (for later steps):
- Missing `message` field
- Empty object `{}`
- Wrong type (example: `{"message": 123}`)
Expected status: `422` with structured validation details.
