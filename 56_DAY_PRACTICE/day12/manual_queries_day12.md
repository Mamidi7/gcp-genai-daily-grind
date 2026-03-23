# Manual Queries / Commands - Day12

Use these manually. Do not mark the day complete until the real output is saved in `api_evidence.txt`.

## 1) Start the service
```bash
cd /Users/krishnavardhan/projects/GCP_GENAI/gcp-genai-daily-grind/56_DAY_PRACTICE/day12
python3 -m uvicorn main:app --host 127.0.0.1 --port 8012
```

Expected startup line:
```text
Uvicorn running on http://127.0.0.1:8012
```

## 2) Health check
```bash
curl -i http://127.0.0.1:8012/health
```

Expected response:
```text
HTTP/1.1 200 OK
...
{"status":"ok"}
```

## 3) Echo valid payload
```bash
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{"message":"hello fastapi"}'
```

Expected response:
```text
HTTP/1.1 200 OK
...
{"echo":"hello fastapi"}
```

## 4) Echo invalid payload
```bash
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{}'
```

Expected response:
```text
HTTP/1.1 422 Unprocessable Entity
...
```

## 5) Optional local verification test
```bash
python3 -m unittest test_main.py -v
```

Expected result:
```text
Ran 3 tests in ...
OK
```

## 6) Save outputs
Paste the actual commands and responses into `api_evidence.txt`.
