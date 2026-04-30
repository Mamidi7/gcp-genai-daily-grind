# Exercise 3: CI/CD Pipeline for Model Serving

## Goal (one line)
Automate testing + deployment so every code change is validated before it reaches production.

## Why This Matters
Interview question: "How do you deploy a model update safely?"
Bad answer: "I run the tests locally and then push."
Good answer: "CI runs lint + unit tests + integration tests on every PR.
If all pass and review is approved, CD builds the Docker image,
runs a smoke test against a staging endpoint, then promotes to production."

## Concept (3-6 lines)
1. CI = Continuous Integration — every push triggers automated tests
2. CD = Continuous Deployment — after tests pass, code deploys automatically
3. For AI: add a "model validation gate" — does the new model pass accuracy checks?
4. GitHub Actions is free for public repos (your repo is public)
5. The pipeline runs in a clean environment — no "works on my machine"
6. Deployment target: Cloud Run (you already did this on Day 10!)

## Architecture

```
git push / PR
     │
     ▼
┌──────────────────────┐
│  GitHub Actions CI    │
│                      │
│  Step 1: Checkout    │
│  Step 2: Setup Python│
│  Step 3: pip install │
│  Step 4: Lint (ruff) │
│  Step 5: Unit Tests  │  ← pytest test_model_api.py
│  Step 6: Build Docker│
│  Step 7: Smoke Test  │  ← curl /healthz inside container
│                      │
│  All pass? ──→ ✅    │
│  Any fail?  ──→ ❌   │  ← PR blocked, notification sent
└──────────────────────┘
         │ (all pass)
         ▼
┌──────────────────────┐
│  CD: Deploy to Cloud │
│  Run (staging)       │
│                      │
│  gcloud run deploy   │
│  --image gcr.io/...  │
│  --region us-central1│
│                      │
│  Smoke test staging  │
│  Promote to prod     │
└──────────────────────┘
```

## What You Build

### 1. `.github/workflows/model-api-ci.yml`
- Trigger: push to main, PR to main
- Jobs: lint → test → build → smoke test
- Uses your existing test_model_api.py

### 2. Model Validation Gate (concept)
- Before deploying a new model version, run eval suite
- If accuracy drops > 5%, block deployment
- This is the AI-specific part of CI/CD

### 3. Deployment Script
- `deploy.sh` — builds Docker, pushes to Artifact Registry, deploys to Cloud Run
- Uses Workload Identity Federation (you already set this up on Day 10!)

## Common Mistake + Fix

Mistake: Running all tests in one giant step.
  Why bad: Hard to debug which layer failed.
  Fix: Separate jobs — lint, test, build. Each fails independently with clear error.

Mistake: No smoke test after deployment.
  Why bad: Deployment succeeds but app is broken (config error, missing env var).
  Fix: After deploy, curl the /healthz and /chat endpoints.

## Check Question
What's the difference between a "model validation gate" and a regular test?
(Answer: regular tests check code correctness. Model validation checks model
quality — accuracy, latency, safety. Both must pass before deploy.)

## Tiny Exercise
1. Read `.github/workflows/model-api-ci.yml`
2. Push a commit to your repo and watch the Action run
3. Intentionally break a test and push — see the red ❌
4. Fix the test and push — see the green ✅
5. Screenshot the GitHub Actions tab for your portfolio
