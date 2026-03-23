# Run Steps

## Step 1 - Go To Day12 Folder
```bash
cd /Users/krishnavardhan/projects/GCP_GENAI/gcp-genai-daily-grind/56_DAY_PRACTICE/day12/practice_session
```

## Step 2 - Start Server
```bash
python3 -m uvicorn 02_main:app --host 127.0.0.1 --port 8012
```

## Step 3 - Test Health Endpoint
Open another terminal and run:

```bash
curl -i http://127.0.0.1:8012/health
```

Expected:
- status code `200`
- body `{"status":"ok"}`

## Step 4 - Test Echo Valid
```bash
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{"message":"hello fastapi"}'
```

Expected:
- status code `200`
- body `{"echo":"hello fastapi"}`

## Step 5 - Test Echo Invalid
```bash
curl -i -X POST http://127.0.0.1:8012/echo \
  -H "content-type: application/json" \
  -d '{}'
```

Expected:
- status code `422`
- error says `message` field is missing

## Forced Failure
Change in `02_main.py`:

```python
message: str
```

to

```python
message: int
```

Then run valid echo again.

Expected:
- validation error because code expects number, but input sends text
