# Day 17 Interview Pack — Embeddings

## 30-Second Version
"I built an embedding pipeline using text-embedding-004 that converts documents to 768-dimensional vectors and retrieves relevant results with cosine similarity. This is the retrieval foundation for my RAG system."

---

## 90-Second STAR Answer

**Situation:** My RAG system needed semantic search — users ask questions in natural language, and keyword matching wasn't cutting it. "How do we handle data quality?" should find the data validation doc, even without exact keyword overlap.

**Task:** I needed to build a text-to-vector pipeline that could embed documents and retrieve the most relevant ones for any query.

**Action:** I built an EmbeddingStore class with three components:
1. **Batch embedder**: Calls text-embedding-004 in batches of 250 with retry logic and empty text filtering
2. **Similarity engine**: Cosine similarity between query vector and all document vectors
3. **Top-k retriever**: Returns ranked results with similarity scores

Key decisions: used cosine similarity over Euclidean distance because we care about semantic direction, not magnitude. Normalized all vectors to unit length. Stored model version alongside embeddings to prevent dimension mismatch.

**Result:** The system correctly retrieves semantically related documents even when query and document share no keywords. Average retrieval latency is dominated by the embedding API call (~200ms), with similarity computation being <1ms for 10K documents.

---

## 3-Minute Technical Deep Dive

### What is an Embedding?
A function that maps text to a point in 768-dimensional space. Similar text ends up near similar points. The model (text-embedding-004) learned this mapping from massive text data.

### Why 768 Dimensions?
Each dimension captures a different semantic feature. Think of it as 768 "meaning axes". The first might capture sentiment, another topic category, another formality level. But they're not interpretable — they're learned features.

### Why Cosine Similarity?
```
Cosine similarity measures the ANGLE between vectors.
It ignores magnitude (vector length).

Example:
  "Banking"  → [0.8, 0.2, 0.1, ...]
  "Finance"  → [0.7, 0.3, 0.1, ...]
  
  These point in a similar direction → high cosine similarity (~0.95)
  Even if one vector is longer than the other.
```

Euclidean distance measures absolute position difference. For normalized vectors, cosine and Euclidean give the same ranking.

### Why Not Just Keyword Search?
```
Query: "How do we handle new records?"
  
Keyword search finds: documents containing "handle", "new", "records"
Misses: "Incremental load processes only new records since last run"
  (has the words, but keyword search doesn't understand context)
  
Also misses: "Watermark-based loading for delta detection"
  (has NONE of the query words, but is the RIGHT answer semantically)
```

### Production Considerations
- **Cost**: text-embedding-004 is ~$0.02 per 1M tokens. Embedding 100K documents ≈ $2.
- **Latency**: Embedding API ~200ms, similarity search ~1ms for in-memory, ~10ms for BigQuery VECTOR_SEARCH
- **Storage**: 768 floats × 4 bytes = 3KB per document embedding. 1M docs = 3GB.
- **Model updates**: Changing embedding model means re-embedding EVERYTHING.

---

## Common Interview Questions

**Q: How do you choose between embedding search and keyword search?**
A: Use embedding search for semantic/natural language queries. Use keyword search for exact matches (product IDs, error codes, names). Production systems often combine both (hybrid search — Day 23).

**Q: What happens when the embedding model is updated?**
A: You must re-embed all documents. Store the model version with embeddings. Plan for migration.

**Q: How do you evaluate embedding quality?**
A: Build a test set of (query, relevant_doc, irrelevant_doc) triples. Measure: does cosine(query, relevant) > cosine(query, irrelevant)? This is what Day 19-20 eval does.
