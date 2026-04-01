# Day 18 Debug Journal

## Error 1: Sentence Splitter Breaks on Abbreviations

**Symptom:** "The U.S. banking system" split into ["The U", "S", "banking system"]
```
regex `(?<=[.!?])\s+` splits on every period
```

**Root Cause:** Simple regex treats every period as sentence end, including abbreviations.

**Fix:** Use a smarter pattern that checks for known abbreviations. Or accept ~5% error rate and handle in chunk merging.

**Prevention:** For production, use spaCy or NLTK sentence tokenizer. For practice, document the limitation.

---

## Error 2: Semantic Chunking Creates Too Many Tiny Chunks

**Symptom:** 20-sentence document → 15 chunks, most with 1-2 sentences
```
similarity_threshold = 0.8 was too aggressive
```

**Root Cause:** Similarity threshold was set too high. Every small topic shift triggered a new chunk.

**Fix:** Lower threshold to 0.3-0.5. Add min_chunk_size enforcement (merge tiny chunks with neighbors).

**Prevention:** Always set both similarity_threshold AND min/max chunk size constraints.

---

## Error 3: Fixed-Size Chunking Cuts Mid-Word

**Symptom:** Chunk ends with "transacti" and next starts with "on processing"
```
Fixed-size at exactly 500 chars cut through "transaction"
```

**Root Cause:** Character-based splitting doesn't know word boundaries.

**Fix:** After splitting, adjust chunk boundary to the nearest space. Or split on words instead of characters.

**Prevention:** Use word-based splitting or adjust boundaries to spaces after character split.

---

## Error 4: Overlap Causes Duplicate Retrieval

**Symptom:** Same content retrieved in top-2 results because it appears in overlap region
```
Chunk 1: "...data quality validation occurs..."
Chunk 2: "...data quality validation occurs after extraction..." (overlap)
```

**Root Cause:** Overlap means the same content exists in multiple chunks. Retrieval finds both.

**Fix:** Deduplicate retrieval results by checking content overlap between returned chunks. Or use smaller overlap (10% instead of 20%).

**Prevention:** Track which source region each chunk covers. Deduplicate by source region overlap.

---

## Key Takeaway
"Chunking is the most impactful RAG hyperparameter. I tested 3 strategies — fixed, sentence, and semantic. Fixed-size with overlap is the production default because it's predictable. The key metrics: chunk count, average size, size variance, and retrieval recall."
