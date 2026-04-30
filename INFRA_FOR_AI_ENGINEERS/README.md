# Infra for AI Engineers — 9 Exercises That Map DevOps to Applied AI

> The classic DevOps interview exercises, translated into what AI/ML roles actually ask.

---

## THE MAPPING

Your standard DevOps checklist vs what an Applied AI engineer needs:

```
Classic DevOps Exercise          →  AI/ML Equivalent (what you actually build)
─────────────────────────────────────────────────────────────────────────────
1. CI/CD pipeline for app        →  CI/CD for model serving (test → validate → deploy)
2. Dockerized app + networking   →  Containerized model API (FastAPI + Gemini + health checks)
3. K8s cluster + deploy service  →  K8s model deployment (GPU requests, rolling updates)
4. Prometheus + Grafana          →  LLM observability (latency, tokens, drift, error rate)
5. ELK / Loki logging            →  LLM request logging (prompt/response trace, PII redaction)
6. Terraform VPC + EC2 + DB     →  Terraform GCP (Vertex AI, Cloud Run, BQ, GCS, IAM)
7. Load balancer + autoscaling   →  Model serving autoscaling (queue depth, GPU utilization)
8. Redis cache + DB fallback     →  Embedding cache + vector DB fallback chain
9. Chaos engineering             →  Model serving chaos (kill model pods, bad inputs, fallback)
```

---

## WHY THIS MATTERS FOR INTERVIEWS

OpenAI B2B Backend Engineer job posting (live March 2026):
  "Architect and maintain services that power AI apps"
  "distributed systems + databases + APIs + data pipelines"
  "Care deeply about reliability, safety, and performance in production"

Anthropic Applied Safety Research Engineer:
  "Build eval pipelines for model training/deployment"
  "Python + data pipelines + LLMs"

Translation: they want people who can make AI systems RELIABLE in production.
Not just call an API and print the response.

---

## CONSTRAINTS

- Zero cost (local Docker/OrbStack only)
- GCP-native where cloud is needed (free tier)
- Every exercise produces: code + debug log + interview answer
- Each exercise fits in one focused session (2-4 hours)

---

## EXERCISE INDEX

| # | Exercise | What You Prove | Key Skill |
|---|----------|---------------|-----------|
| 1 | Model Serving API + Tests | You can ship a model endpoint | FastAPI + pytest |
| 2 | Dockerized Model API | You can containerize AI services | Docker + health checks |
| 3 | CI/CD for Model Deploy | You automate testing + deployment | GitHub Actions |
| 4 | LLM Observability Stack | You monitor model behavior in prod | metrics + dashboards |
| 5 | Request Logging Pipeline | You trace every LLM call | structured logging |
| 6 | Terraform GCP Infra | You define infra as code for AI | Terraform + GCP |
| 7 | Autoscaling Model Serving | You handle traffic spikes | K8s/HPA or Cloud Run |
| 8 | Cache + Fallback Chain | You make retrieval resilient | Redis + vector DB |
| 9 | Chaos Engineering for AI | You test failure modes | fault injection |

---

## HOW TO USE THIS

1. Start with Exercise 1 (it's the foundation everything else builds on)
2. Each exercise has its own folder with:
   - `exercise.md` — what to build
   - `solution/` — reference implementation
   - `debug_journal.md` — things that break and how to fix them
   - `interview_answers.md` — how to talk about it
3. Complete all 9 = you can answer any "how would you deploy this in prod?" question

---

## INTERVIEW SOUND BITES (Use These)

30-second version:
  "I built a containerized model serving API with health checks,
   deployed it via CI/CD, added observability for latency and token usage,
   and tested failure modes including model fallback chains."

90-second STAR:
  "In my production-style project, I containerized a FastAPI model serving
   endpoint with Docker. I added a CI/CD pipeline that runs integration tests
   before deployment. For observability, I tracked per-request latency, token
   usage, and error rates. When I simulated model API failures, my fallback
   chain kept responses flowing through a cached result path. The key lesson
   was that model serving needs the same reliability engineering as any
   distributed system — plus extra care for non-deterministic outputs."
