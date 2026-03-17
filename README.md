# GCP AI/ML Learning Journey

Structured 56-day preparation for GCP AI/ML Engineer role.

## The Story

Transitioning from banking ETL (Data Engineering) to GCP AI/ML after a career gap. This repository documents my hands-on learning path - not tutorials followed passively, but real projects built from scratch.

## 56-Day Structure

| Phase | Days | Focus |
|-------|------|-------|
| Foundation | 1-14 | Python, SQL, BigQuery, Vertex AI basics |
| Project 1 | 15-28 | Self-Correcting RAG with LangChain + Vertex AI |
| Project 2 | 29-42 | MLOps Pipeline with Vertex AI Endpoints |
| Interview | 43-56 | System design, behavioral questions |

## Projects

### Self-Correcting RAG
- Built retrieval system with LangChain
- Evaluation with RAGAs metrics
- Deployed on Vertex AI

### MLOps Pipeline
- Training pipeline with Vertex AI Training
- Model versioning with Vertex AI Model Registry
- CI/CD with GitHub Actions to Cloud Run

### Fine-Tuning
- LoRA fine-tuning on custom datasets
- Experiment tracking with Vertex AI Experiments

## Daily Format

Each day follows the same structure:
```
dayX/
├── script.py      # Code I wrote
├── notes.md       # What I learned
├── exercises.py   # Practice problems
└── solution.py    # When I solve it
```

## Interview Delivery System (CODE-LENS)

To avoid line-by-line memorization and improve interview explanation quality, this repo includes a standard process:

1. Read [docs/CODE_LENS_STANDARD.md](docs/CODE_LENS_STANDARD.md)
2. Use templates in `docs/templates/`
3. Start a daily session with:

```bash
bash scripts/start_code_lens_session.sh
```

This generates `docs/code_lens_sessions/session_YYYY-MM-DD.md` with:
- CodeCard
- BugCard
- InterviewPack (30s/90s/3min)
- QuestionBank

## Tech Stack

- **Languages:** Python, SQL
- **Cloud:** GCP (BigQuery, Vertex AI, Cloud Run, Cloud Functions)
- **ML/AI:** LangChain, LangGraph, Hugging Face, Gemma
- **MLOps:** Docker, GitHub Actions, Kubeflow Pipelines

## Why This Matters

1. **Consistency** - 56 days of daily commits shows commitment
2. **End-to-end** - Not just snippets, but full projects
3. **GCP-native** - Using Vertex AI the "real way", not just API calls

## Connect

- GitHub: github.com/Mamidi7
- LinkedIn: linkedin.com/in/krishnavardhan

---
*Last updated: March 2026*
