# Debug Journal — Day 16

## Error / Symptom
Recursive chunking produced `char_start`/`char_end` values that did not point to the original text.
Example: chunk text was `"Google Cloud Platform..."` but `char_start` was 0 and `char_end` was 47 for first chunk, then 48+ for next — but the actual text had variable spacing after sentence boundaries.

## Root Cause
`re.split(r"(?<=[.!?])\s+", text)` consumes the whitespace between sentences.
The code incremented `char_cursor` by `len(snippet) + 1`, assuming exactly one space between chunks.
This assumption was false when multiple spaces or newlines existed.

## Fix
Replaced manual cursor arithmetic with `text.find(snippet)` to locate the exact position in the source text.
If `find()` returns -1 (duplicate text), fall back to 0.

```python
start = text.find(snippet)
end = start + len(snippet) if start != -1 else -1
```

## Prevention
1. Any metadata that claims to point into source text must be tested against the source.
2. Prefer deterministic lookups (`find`, `index`) over manual cursor math when whitespace is involved.
3. Add a test that asserts `SAMPLE[c.char_start:c.char_end] == c.text` for every chunk.

## Impact
Chunk metadata is now trustworthy. If a downstream system highlights the chunk in the original document, it will highlight the correct region. Without this fix, citations and UI highlights would land on wrong text.
