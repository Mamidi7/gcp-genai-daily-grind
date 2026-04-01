# Day 17 Debug Journal

## Error 1: Zero Vector in Embedding Response

**Symptom:** `ZeroDivisionError` in cosine similarity
```
magnitude of vector = 0.0 → division by zero
```

**Root Cause:** Empty or whitespace-only text was passed to embedding API, returning a zero vector.

**Fix:** Filter empty texts before embedding. Check magnitude before computing similarity. Return 0.0 similarity for zero vectors.

**Prevention:** Always validate input text is non-empty before calling embedding API. Log skipped texts.

**Impact:** Prevents crashes in retrieval pipeline. Every RAG system needs this guard.

---

## Error 2: Batch Size Exceeds API Limit

**Symptom:** `400 Bad Request: batch size exceeds maximum of 250`
```
Attempted to embed 500 texts in one call.
```

**Root Cause:** text-embedding-004 has a 250 text per request limit.

**Fix:** Split into batches of 250 with `batch_embed_with_retry()`. Auto-split any oversized batch.

**Prevention:** Always use the batch helper, never call embed() directly with unbounded lists.

---

## Error 3: Dimension Mismatch Between Query and Index

**Symptom:** `ValueError: Dimension mismatch: 768 vs 256`
```
Query embedded with text-embedding-preview-0409 (256 dims)
Index built with text-embedding-004 (768 dims)
```

**Root Cause:** Different embedding models produce different dimension vectors. You cannot compare vectors from different models.

**Fix:** Store the model name alongside embeddings. Validate model consistency at query time.

**Prevention:** Pin the embedding model in config. Never change models without re-embedding everything.

---

## Error 4: Similarity Score Meaning Confusion

**Symptom:** "Why is the similarity 0.85 but the results look wrong?"
```
Cosine similarity with un-normalized vectors gave inflated scores.
```

**Root Cause:** text-embedding-004 returns normalized vectors (unit length), but custom embeddings might not be. Cosine similarity assumes meaningful magnitudes.

**Fix:** Always normalize vectors to unit length before storing. Verify with `magnitude ≈ 1.0`.

**Prevention:** Add normalization step after every embedding call. Add a unit test that checks magnitude.

---

## Key Takeaway

"Embeddings convert text to vectors. Cosine similarity finds the angle between vectors — close angles mean similar meaning. The 3 gotchas: empty inputs give zero vectors, batch sizes must be ≤ 250, and you can never mix embedding models."
