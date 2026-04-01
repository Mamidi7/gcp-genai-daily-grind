# Day 18 — Chunking Strategies: 3 Approaches + Recall Comparison

## Objective
Implement and compare 3 text chunking strategies for RAG pipelines. Understand how chunk size, overlap, and strategy affect retrieval quality.

## Why This Matters
- Chunking is the MOST underrated part of RAG
- Bad chunking = bad retrieval = bad answers, no matter how good your LLM is
- Interview differentiator: "I compared fixed, sentence, and semantic chunking and measured recall"

## The 3 Strategies
```
┌───────────────────────────────────────────────────────────┐
│ 1. FIXED-SIZE CHUNKING                                    │
│    Split every N characters with overlap                  │
│    ✅ Simple, predictable size                            │
│    ❌ Cuts sentences in half, loses context               │
│                                                           │
│ 2. SENTENCE-BASED CHUNKING                                │
│    Split on sentence boundaries, group into chunks        │
│    ✅ Respects sentence boundaries                        │
│    ❌ Variable size, may be too short or too long         │
│                                                           │
│ 3. SEMANTIC CHUNKING                                      │
│    Group sentences by embedding similarity                │
│    ✅ Keeps related content together                      │
│    ❌ Requires embedding calls (cost + latency)           │
└───────────────────────────────────────────────────────────┘
```

## Files
- `solution.py` — All 3 chunking strategies + comparison
- `exercises.py` — Practice challenges
- `notes.md` — Debug journal and interview prep

## Interview Conversion
- **30s**: "I compared 3 chunking strategies for RAG — fixed-size, sentence-based, and semantic. Semantic chunking had the best recall but costs more. Fixed-size is the production default because it's predictable."
- **90s STAR**: See interview_pack_day18.md
