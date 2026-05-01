# Interview Pack — Day 16

## 30-second pitch
I built three chunking strategies — fixed-size, recursive sentence-aware, and semantic paragraph-aware — for a RAG ingestion pipeline, with Pydantic V2 validation and a cosine-similarity retrieval baseline. I debugged and fixed a character-position drift bug caused by regex whitespace consumption.

## 90-second STAR answer
**Situation:** Building a RAG pipeline, needed to split documents into chunks before embedding and retrieval.
**Task:** Implement chunking that preserves meaning boundaries and produces verifiable metadata (char positions).
**Action:**
- Built fixed-size for speed, recursive for sentence preservation, semantic for paragraph preservation.
- Added Pydantic V2 models with field validators.
- Discovered char positions were drifting in recursive chunks because `re.split` consumed whitespace and my cursor math assumed 1 space.
- Fixed by replacing manual arithmetic with `text.find()`.
- Wrote pytest tests that assert every chunk exists exactly in the source text.
**Result:** Retrieval baseline runs locally with deterministic fake embeddings, chunk metadata is trustworthy, and tests guard against regression.

## 3-minute deep dive
**Tradeoffs:**
- Fixed-size is O(n) and cache-friendly but cuts mid-sentence. Use when speed matters more than boundary preservation.
- Recursive is better for meaning but variable chunk size complicates batch embedding.
- Semantic is ideal for structured docs but fails if paragraphs are missing or oversized; we added recursive fallback.

**Why cosine similarity:**
- Embeddings from the same model live on the unit hypersphere (normalized).
- Cosine measures direction, not magnitude, so document length doesn't skew scores.
- For positive-only embeddings, cosine range is [0, 1], which is intuitive.

**Why Pydantic V2:**
- `Field(min_length=1, pattern=...)` validates at instantiation, catching bad data before it reaches the vector DB.
- `@field_validator` with `@classmethod` is the V2 pattern; V1 `@validator` is deprecated.

**Production next step:**
- Replace `embed_fake` with Vertex AI `text-embedding-004`.
- Store chunks in BigQuery with `VECTOR_SEARCH()` for retrieval.
- Add token counting with `tiktoken` or model-specific tokenizer instead of `len/4` estimate.

## Anticipated questions
Q: What happens if a chunk is larger than the embedding model's context window?
A: We validate `token_estimate` at chunk time and can reject or re-split. Currently using a rough `len/4` estimate; production would use the exact tokenizer.

Q: How do you handle duplicate text in `find()`?
A: For duplicate snippets, `find()` returns the first match. In production I'd assign a unique chunk ID at split time rather than relying on char positions for identity.

Q: Why not use LangChain's text splitters?
A: For interview depth, I want to own the logic and tradeoffs. Built-in splitters hide the boundary rules, which makes debugging harder when retrieval quality drops.
