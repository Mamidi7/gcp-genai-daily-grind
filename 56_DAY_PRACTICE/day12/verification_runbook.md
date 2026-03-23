# Day12 Verification Runbook

## Start Server
```bash
cd /Users/krishnavardhan/projects/GCP_GENAI/gcp-genai-daily-grind/56_DAY_PRACTICE/day12
python3 -m uvicorn main:app --host 127.0.0.1 --port 8012
```

## Test 1 - Health Endpoint
```bash
curl -sS http://127.0.0.1:8012/health
```
Expected:
```json
{"status":"ok"}
```

## Test 2 - Echo Endpoint (valid)
```bash
curl -sS -X POST http://127.0.0.1:8012/echo \
  -H 'content-type: application/json' \
  -d '{"message":"hello fastapi"}'
```
Expected:
```json
{"echo":"hello fastapi"}
```

## Test 3 - Echo Endpoint (invalid)
```bash
curl -sS -X POST http://127.0.0.1:8012/echo \
  -H 'content-type: application/json' \
  -d '{}'
```
Expected:
- `422` validation response from FastAPI.

## Evidence Capture
Store request/response logs in:
- `day12/api_evidence.txt`
