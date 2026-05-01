# Day 16 — Chunking Strategies + Cosine Similarity Baseline

## Objective
Implement three text chunking strategies for RAG and a local cosine-similarity retrieval baseline.

## Files
- `chunking_strategies.py` — main implementation (runnable, zero placeholders)
- `test_chunking_strategies.py` — pytest suite (17 tests, all passing)
- `notes.md` — concept summary
- `debug_journal_day16.md` — char-position drift bug
- `interview_pack_day16.md` — 30s, 90s STAR, 3-min deep dive

## Run
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 chunking_strategies.py
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m pytest test_chunking_strategies.py -v
```

## What it does
1. Splits text into chunks using fixed-size, recursive sentence-aware, or semantic paragraph-aware strategies.
2. Validates every chunk with Pydantic V2 (no empty text, valid char bounds, known strategy).
3. Embeds chunks with deterministic fake embeddings (no API cost).
4. Retrieves top-k chunks by cosine similarity, with optional score threshold.

## Debug story
Recursive chunking char positions drifted because `re.split` consumed whitespace and cursor math assumed 1 space. Fixed by using `text.find()` and validated with tests.
