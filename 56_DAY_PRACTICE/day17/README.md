# Day 17 — Embeddings Intro: text-embedding-004 + Similarity Search

## Objective
Build an embedding pipeline that converts text to vectors and performs similarity search. This is the foundation for all RAG systems.

## Why This Matters
- Embeddings are how machines "understand" text meaning
- Every RAG pipeline (Day 21-24) depends on this
- Interview question: "Explain embeddings in 60 seconds" — you WILL be asked this
- Directly connects to BigQuery Vector Search (Shock Topic #2)

## Architecture
```
Text Documents
     │
     ▼
┌──────────────┐
│ Embedding API│  ← text-embedding-004 (768 dimensions)
│ Batch Call   │     5 texts per call, with rate limiting
└──────┬───────┘
       │ list of float vectors
       ▼
┌──────────────┐
│ Similarity   │  ← cosine similarity between all pairs
│ Matrix       │     finds most similar documents
└──────┬───────┘
       │ ranked results
       ▼
┌──────────────┐
│ Retrieval    │  ← given a query, find top-k most similar
│ Function     │     this IS the R in RAG
└──────────────┘
```

## Files
- `solution.py` — Full working embedding pipeline (mock + real modes)
- `exercises.py` — Practice challenges
- `notes.md` — Concepts and interview prep
- `debug_journal_day17.md` — Error artifacts
- `interview_pack_day17.md` — STAR answers

## Prerequisites
- `numpy` installed
- Real Gemini: set `GOOGLE_CLOUD_PROJECT` + Vertex AI enabled
- Mock mode: works with zero dependencies beyond numpy

## Interview Conversion
- **30s**: "I built an embedding pipeline using text-embedding-004 that converts documents to 768-dimensional vectors and performs cosine similarity retrieval. This is the retrieval layer for my RAG system."
- **90s STAR**: "My RAG system needed semantic search, not keyword search. I built an embedding pipeline that batch-calls the text-embedding-004 model, stores vectors, and retrieves top-k results by cosine similarity. The key learning: embedding model choice and batch size both affect retrieval quality and cost significantly."
