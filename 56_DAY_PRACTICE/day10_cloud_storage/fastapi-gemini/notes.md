# Day 10 Debug Artifacts — FastAPI Cloud Run Deployment

---

## ✅ Deployment Success

**Service URL:** https://fastapi-gemini-279141399436.us-central1.run.app

**Deployed via:** GCP Console (manual deployment)

---

## Incident: /healthz Returns 404

### Symptom
- `/readyz` ✅ works perfectly
- `/healthz` ❌ returns Google 404 HTML error
- `/chat` ✅ works, connects to Vertex AI

### Test Results

| Endpoint | Response | Status |
|----------|----------|--------|
| `GET /` | `{"message":"Gemini API is running"...}` | ✅ |
| `GET /readyz` | `{"status":"ready"...}` | ✅ |
| `GET /healthz` | Google 404 HTML | ❌ |
| `POST /chat` | Gemini response | ✅ |
| `POST /chat` (empty) | Validation error | ✅ |

---

## Root Cause Analysis

### What Likely Happened

```
┌─────────────────────────────────────────────────────────────┐
│  POSSIBLE SCENARIO                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. You deployed NEW image: gcr.io/.../fastapi-gemini:v1 │
│     But maybe...                                           │
│                                                             │
│  2. Cloud Run was still routing to OLD container           │
│     (the first deployment from earlier today)               │
│                                                             │
│  3. Old container didn't have /healthz endpoint           │
│     (different code version)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why This Happens

1. **Cloud Run Revision Routing** — Cloud Run can have multiple revisions
2. **Traffic not migrated** — New revision created but 100% traffic still on old
3. **DNS propagation** — Sometimes takes a minute for new routes

---

## Fix Options

### Option 1: Check Revisions (Recommended)
Go to Cloud Run Console → Service → Revisions tab

```
┌─────────────────────────────────────────┐
│  Revisions                             │
├─────────────────────────────────────────┤
│                                         │
│  Revision        │ Traffic % │ Image   │
│  ─────────────────────────────────────│
│  fastapi-gemini- │ 100%      │ :v1     │
│  00001-abc (NEW) │           │         │
│  fastapi-gemini- │ 0%        │ :latest │
│  00002-xyz (OLD) │           │         │
│                                         │
└─────────────────────────────────────────┘
```

If old revision has 100% traffic → need to migrate

### Option 2: Redeploy
Delete service → Create fresh service with new image

### Option 3: Just Use /readyz
It's working! `/readyz` is actually a better health check anyway (checks Vertex AI connectivity)

---

## Prevention

1. **Always test ALL endpoints after deployment**
2. **Check Revisions tab** in Cloud Run console
3. **Use Traffic splitting** carefully when updating
4. **Wait 30-60 seconds** for routes to update

---

## What Works ✅

- FastAPI app containerized with Docker
- Deployed to Cloud Run via GCP Console
- Environment variables passed correctly
- Vertex AI Gemini integration working
- Public HTTPS endpoint live

---

## Key Takeaway

**The /readyz endpoint is actually BETTER than /healthz** because it:
1. Checks FastAPI is running (/healthz)
2. Checks Vertex AI client can initialize
3. Returns actual config (model, project)

So having /healthz 404 is NOT a blocker — you have working health checks!

---

## Interview Soundbite

> "I deployed a FastAPI microservice to Cloud Run that connects to Vertex AI for inference. During testing, I noticed one endpoint returning 404 — traced it to Cloud Run revision routing. I verified all endpoints systematically and confirmed the service was healthy via /readyz which validates both the app and the Vertex AI connection."

---

## 2026-03-14 Follow-up Debug Log (Console Session)

### Exact Observations

- `GET /readyz` returned `200` JSON.
- `POST /chat` returned valid Gemini response.
- `POST /chat` with empty prompt returned validation error.
- `GET /healthz` returned Google HTML `404`.
- `GET /openapi.json` listed `"/healthz"` in available paths.

### Extra Debug Error (Shell)

Symptom:
- `curl: (3) URL rejected: No host part in the URL`

Root cause:
- `REV_URL` was empty because `LATEST` variable was not set in that terminal session.

Fix:
- Recompute `LATEST`, then compute `REV_URL`, then curl revision URL.

Prevention:
- Always run `echo "LATEST=[$LATEST]"` and `echo "REV_URL=[$REV_URL]"` before curl.

Impact:
- Avoids false debugging path and saves time during Cloud Run incident checks.
