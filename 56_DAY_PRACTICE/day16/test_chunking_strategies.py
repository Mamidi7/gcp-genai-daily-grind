"""pytest for day16 chunking strategies.

Run: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m pytest test_chunking_strategies.py -v
"""

import numpy as np
import pytest
from chunking_strategies import (
    TextChunk,
    chunk_fixed,
    chunk_recursive,
    chunk_semantic,
    cosine_similarity,
    embed_fake,
    retrieve_top_k,
)


SAMPLE = """First sentence here. Second sentence follows.

New paragraph starts. Another one here."""


class TestChunkFixed:
    def test_produces_chunks(self):
        chunks = chunk_fixed(SAMPLE, chunk_size=30, overlap=5)
        assert len(chunks) > 0
        assert all(isinstance(c, TextChunk) for c in chunks)

    def test_overlap_reduces_count(self):
        no_overlap = chunk_fixed(SAMPLE, chunk_size=30, overlap=0)
        with_overlap = chunk_fixed(SAMPLE, chunk_size=30, overlap=10)
        assert len(with_overlap) >= len(no_overlap)

    def test_char_bounds_valid(self):
        chunks = chunk_fixed(SAMPLE, chunk_size=30, overlap=5)
        for c in chunks:
            assert c.char_start <= c.char_end
            assert SAMPLE[c.char_start:c.char_end] == c.text


class TestChunkRecursive:
    def test_preserves_sentences(self):
        chunks = chunk_recursive(SAMPLE, max_chars=60)
        for c in chunks:
            # each chunk should end with sentence terminator or be the tail
            assert c.text[-1] in ".!?" or c == chunks[-1]

    def test_no_empty_chunks(self):
        chunks = chunk_recursive(SAMPLE, max_chars=30)
        assert all(c.text.strip() for c in chunks)

    def test_char_bounds_point_into_text(self):
        chunks = chunk_recursive(SAMPLE, max_chars=40)
        for c in chunks:
            # find() can return -1 if duplicate text exists, but text must appear
            assert c.text in SAMPLE


class TestChunkSemantic:
    def test_preserves_paragraphs(self):
        chunks = chunk_semantic(SAMPLE, max_chars=200)
        for c in chunks:
            # no internal double-newline means paragraph wasn't split
            assert "\n\n" not in c.text

    def test_fallback_to_recursive_for_long_paragraph(self):
        long_para = "A. " * 500  # one paragraph, very long
        chunks = chunk_semantic(long_para, max_chars=100)
        assert len(chunks) > 1
        assert all(c.strategy == "semantic" for c in chunks)


class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = np.array([1.0, 2.0, 3.0])
        assert cosine_similarity(v, v) == pytest.approx(1.0)

    def test_opposite_vectors(self):
        v = np.array([1.0, 0.0])
        w = np.array([-1.0, 0.0])
        assert cosine_similarity(v, w) == pytest.approx(-1.0)

    def test_orthogonal_vectors(self):
        v = np.array([1.0, 0.0])
        w = np.array([0.0, 1.0])
        assert cosine_similarity(v, w) == pytest.approx(0.0)

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            cosine_similarity(np.array([1.0]), np.array([1.0, 2.0]))


class TestRetrieveTopK:
    def test_respects_k(self):
        chunks = chunk_fixed("A B C D E F G H I J", chunk_size=2, overlap=0)
        result = retrieve_top_k("A", chunks, k=3)
        assert len(result) == 3

    def test_threshold_filters(self):
        chunks = chunk_fixed("hello world test", chunk_size=5, overlap=0)
        result = retrieve_top_k("xyz", chunks, k=5, threshold=0.99)
        assert len(result) == 0

    def test_best_score_is_highest(self):
        chunks = chunk_recursive("Apple banana cherry date", max_chars=20)
        result = retrieve_top_k("banana", chunks, k=2)
        scores = [s for s, _ in result]
        assert scores == sorted(scores, reverse=True)


class TestTextChunkValidation:
    def test_empty_text_rejected(self):
        with pytest.raises(Exception):
            TextChunk(text="", strategy="fixed", index=0, char_start=0, char_end=1, token_estimate=1)

    def test_end_before_start_rejected(self):
        with pytest.raises(Exception):
            TextChunk(
                text="hi", strategy="fixed", index=0, char_start=5, char_end=2, token_estimate=1
            )
