# Day 17 Notes

## What I built today
- Mock embedding client that simulates text-embedding-004 (768 dimensions)
- Deterministic vector generation (same text → same vector, simulates real behavior)
- Cosine similarity, Euclidean distance, and dot product functions
- EmbeddingStore class with index() and search() methods
- Batch embedding utility with retry and empty text filtering
- Full similarity matrix computation

## Key concepts learned
1. **Embeddings**: Convert text → 768 float numbers. Similar text → similar numbers.
2. **Cosine similarity**: Measures angle between vectors. 1.0 = identical, 0.0 = unrelated.
3. **Batch embedding**: API limit is 250 texts per call. Always batch.
4. **Normalization**: Real embedding models return unit vectors (magnitude = 1.0).

## Error I hit
- Zero vector on empty text input → division by zero in cosine similarity
- Dimension mismatch when comparing vectors from different models

## Root cause
- Input validation was missing — no check for empty strings
- Model version not stored alongside embeddings

## Fix applied
- Filter empty texts before embedding
- Store model name in EmbeddingResult metadata
- Check vector magnitude before similarity computation

## Prevention added
- `batch_embed_with_retry()` handles all edge cases
- Unit vector validation in test suite

## 90-second interview version
"I built a semantic search engine using text-embedding-004. Documents get converted to 768-dimensional vectors, and retrieval uses cosine similarity to find the most relevant matches. I learned three critical production lessons: filter empty inputs to prevent zero-vector crashes, respect the 250-text batch limit, and never mix embedding models without re-indexing."

## How this connects to the sprint
- Day 17 = embedding foundation
- Day 18 = chunking (how to split documents BEFORE embedding)
- Day 21 = BigQuery Vector Search (production version of this store)
- Day 19-20 = eval harness will test retrieval quality
