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

## Interview Signal Engine

To convert daily work into hiring evidence, use:

`56_DAY_PRACTICE/interview_signal/`

Daily execution source of truth:

`56_DAY_PRACTICE/DAILY_PREP_MAIN.md`

Primary external directive source:

`/Users/krishnavardhan/projects/GCP_GENAI/_INTERVIEW_PREP/OPENAI_ANTHROPIC_APPLIED_AI_DIRECTIVES_2026-03-15/00_COREST_CORE_FILE.md`

This includes:

- 14-day execution tracker (30-min tool block)
- Daily artifact template (build + fail + fix + STAR)
- Debug journal template (symptom -> root cause -> prevention)
- Interview pack template (30s, 90s STAR, 3-min walkthrough)
- Tool usage matrix for roadmap/debug/API/portfolio/speaking tools

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
