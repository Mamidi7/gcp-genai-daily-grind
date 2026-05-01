# Day 16 — Chunking Strategies + Cosine Similarity Baseline

## What we built
Three chunking strategies for RAG text preprocessing, plus a local cosine-similarity retrieval baseline.

## 3 Strategies

| Strategy | How | Best for | Risk |
|----------|-----|----------|------|
| Fixed-size | Sliding window by char count | Speed, uniform size | Cuts mid-sentence, loses context |
| Recursive | Sentence-aware group | Preserves meaning boundaries | Slightly slower, variable size |
| Semantic | Paragraph-aware + recursive fallback | Documents with clear sections | Needs clean paragraph breaks |

## Cosine Similarity
- Measures angle between two vectors, not magnitude.
- Range: -1 (opposite) to 1 (identical).
- For embeddings, usually 0 to 1 because all values are positive.

## Key Validation
- TextChunk uses Pydantic V2: min_length, ge, pattern regex.
- char_start/char_end validated so end >= start.
- Tests verify chunks actually exist inside the original text.

## Debug story (captured in debug_journal_day16.md)
Recursive chunk char positions drifted because manual cursor increment didn't account for regex-consumed whitespace. Fixed by using text.find().

## Interview 30-second pitch
"I built three chunking strategies for a RAG pipeline — fixed, recursive sentence-aware, and semantic paragraph-aware — with Pydantic validation and a cosine-similarity retrieval baseline. I caught a metadata drift bug where character positions became invalid because whitespace consumption wasn't tracked, and I fixed it with source-text lookup plus tests."
