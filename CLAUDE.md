# gcp-genai-daily-grind — Krishna's Interview Prep Repo

## Purpose
Daily practice repo for GCP AI/ML + Applied AI interview preparation.
Every day should produce at least one commit with real, runnable code.

## Repo Structure
- 56_DAY_PRACTICE/ — daily practice folders (Day_01 through Day_56+)
- 56_DAY_PRACTICE/DAILY_PREP_MAIN.md — master tracker
- 56_DAY_PRACTICE/interview_signal/ — execution tracker

## Rules
1. Each day folder must have at least one .py file that actually runs
2. Code must include comments explaining the concept
3. Follow the 47-day sprint plan from:
   /Users/krishnavardhan/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/OPTIMIZED_47_DAY_SPRINT_PLAN.md
4. Commit message format: "Day XX: topic — brief description"
5. Never push empty or scaffold-only files

## Priority Topics
1. Structured output (Pydantic + Gemini)
2. Embeddings + similarity search
3. Chunking strategies
4. Evaluation metrics (exact match, BLEU, semantic)
5. RAG pipeline (retrieval + generation)
6. FastAPI endpoints
7. GCP service integration (Vertex AI, BigQuery)
8. Agent/tool-use patterns

## Style
- Simple Python, well-commented
- Each script should be self-contained and runnable with `python filename.py`
- Print output that demonstrates the concept working
- Include edge case handling where appropriate
