"""
Day 20 - Eval Harness v3 (Interview-Grade)
Goal: Multi-metric RAG evaluation with real failure detection.
Run: python eval_harness_v3.py
Output: JSON report + human summary

Metrics:
  1. keyword_score  — % of expected keywords found in answer
  2. citation_ok    — expected citation present in answer
  3. faithfulness   — answer doesn't contradict the source context
  4. relevance      — answer actually addresses the question
  5. length_ok      — answer is within sane bounds (not too short, not too long)
  6. no_answer_det  — "I don't know" detection for unanswerable questions
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class EvalCase:
    name: str
    question: str
    expected_keywords: List[str]
    expected_citations: List[str]
    source_context: str           # the retrieved context (for faithfulness check)
    min_keyword_score: float = 0.5
    min_answer_chars: int = 20    # floor for length check
    max_answer_chars: int = 2000  # ceiling for length check
    is_unanswerable: bool = False  # if True, answer should be "I don't know"


@dataclass
class EvalResult:
    case_name: str
    passed: bool
    keyword_score: float
    citation_ok: bool
    faithfulness_ok: bool
    relevance_ok: bool
    length_ok: bool
    no_answer_correct: bool      # True if unanswerable detected correctly
    failure_reasons: List[str]


# ── Metric Functions ──────────────────────────────────────────────

def keyword_score(answer: str, keywords: List[str]) -> float:
    """% of expected keywords found in answer (case-insensitive)."""
    if not keywords:
        return 1.0
    ans = answer.lower()
    hit = sum(1 for k in keywords if k.lower() in ans)
    return round(hit / len(keywords), 2)


def citation_ok(answer: str, citations: List[str]) -> bool:
    """At least one expected citation found in answer."""
    if not citations:
        return True  # no citation expected
    ans = answer.lower()
    return any(c.lower() in ans for c in citations)


def faithfulness_ok(answer: str, source_context: str) -> bool:
    """
    Check if answer contradicts source context.
    Simple heuristic: key entities in answer should appear in context.
    """
    if not source_context:
        return True  # no context to check against
    # Extract capitalized words and numbers as "entities"
    ans_entities = set(re.findall(r'\b[A-Z][a-z]+\b', answer))
    ctx_entities = set(re.findall(r'\b[A-Z][a-z]+\b', source_context))
    if not ans_entities:
        return True
    overlap = ans_entities & ctx_entities
    # At least 30% of answer entities should appear in source
    ratio = len(overlap) / len(ans_entities) if ans_entities else 1.0
    return ratio >= 0.3


def relevance_ok(answer: str, question: str) -> bool:
    """
    Check if answer addresses the question.
    Simple heuristic: key question words appear in answer.
    """
    q_words = set(re.findall(r'\b\w{4,}\b', question.lower()))
    a_words = set(re.findall(r'\b\w{4,}\b', answer.lower()))
    # Remove common stop words
    stop = {"what", "why", "how", "does", "that", "this", "with", "from", "which"}
    q_words -= stop
    if not q_words:
        return True
    overlap = q_words & a_words
    return len(overlap) / len(q_words) >= 0.3


def length_ok(answer: str, min_chars: int, max_chars: int) -> bool:
    """Answer length within sane bounds."""
    return min_chars <= len(answer) <= max_chars


def no_answer_detected(answer: str) -> bool:
    """Detect if the model says 'I don't know' or equivalent."""
    patterns = [
        r"i don'?t know",
        r"i am not sure",
        r"i cannot answer",
        r"no information",
        r"not mentioned",
        r"not available",
        r"unknown",
    ]
    ans = answer.lower()
    return any(re.search(p, ans) for p in patterns)


# ── Core Evaluation ───────────────────────────────────────────────

def evaluate_one(case: EvalCase, answer: str) -> EvalResult:
    k_score = keyword_score(answer, case.expected_keywords)
    c_ok = citation_ok(answer, case.expected_citations)
    f_ok = faithfulness_ok(answer, case.source_context)
    r_ok = relevance_ok(answer, case.question)
    l_ok = length_ok(answer, case.min_answer_chars, case.max_answer_chars)
    no_ans = no_answer_detected(answer)

    # For unanswerable questions: the CORRECT behavior is to say "I don't know"
    if case.is_unanswerable:
        no_ans_correct = no_ans  # should detect "I don't know"
        passed = no_ans_correct
    else:
        no_ans_correct = not no_ans  # should NOT say "I don't know" for answerable Qs
        passed = (
            k_score >= case.min_keyword_score
            and c_ok
            and f_ok
            and r_ok
            and l_ok
            and no_ans_correct
        )

    # Collect failure reasons
    reasons = []
    if k_score < case.min_keyword_score:
        reasons.append(f"low keyword score ({k_score})")
    if not c_ok:
        reasons.append("missing citation")
    if not f_ok:
        reasons.append("possible hallucination (entities not in source)")
    if not r_ok:
        reasons.append("answer doesn't address question")
    if not l_ok:
        reasons.append(f"bad length ({len(answer)} chars)")
    if case.is_unanswerable and not no_ans:
        reasons.append("should have said 'I don't know'")
    if not case.is_unanswerable and no_ans:
        reasons.append("said 'I don't know' for an answerable question")

    return EvalResult(
        case_name=case.name,
        passed=passed,
        keyword_score=k_score,
        citation_ok=c_ok,
        faithfulness_ok=f_ok,
        relevance_ok=r_ok,
        length_ok=l_ok,
        no_answer_correct=no_ans_correct,
        failure_reasons=reasons if reasons else ["-"],
    )


# ── Fake RAG (replace with real model call) ───────────────────────

def fake_rag_answer(question: str) -> str:
    """Simulated RAG responses. Replace with real Gemini call."""
    bank = {
        "What is RAG?": (
            "RAG stands for Retrieval Augmented Generation. It retrieves relevant "
            "documents from a knowledge base before generating an answer. This grounds "
            "the model's response in real data and reduces hallucination. "
            "Source: doc_rag_intro.md"
        ),
        "Why chunking matters?": (
            "Chunking breaks documents into smaller pieces for more precise retrieval. "
            "Good chunking preserves context boundaries and improves retrieval precision. "
            "Bad chunking can split important information across chunks. "
            "Source: doc_chunking_notes.md"
        ),
        "What is hallucination control?": (
            "Hallucination control uses grounding, citations, and confidence thresholds "
            "to reduce unsupported claims in LLM outputs. Key techniques include "
            "retrieval augmentation and source verification. "
            "Source: doc_reliability.md"
        ),
        "What is the capital of France?": (
            "Paris is the capital of France. This is basic geography. "
            "Source: unknown"
        ),
    }
    return bank.get(question, "I don't know. The information is not available in the provided context.")


# ── Suite Runner ──────────────────────────────────────────────────

def run_suite(cases: List[EvalCase]) -> Dict:
    results = []
    for case in cases:
        ans = fake_rag_answer(case.question)
        results.append(evaluate_one(case, ans))

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    pass_rate = round(passed / total, 2) if total else 0.0

    return {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": pass_rate,
        "results": [asdict(r) for r in results],
    }


def print_report(report: Dict) -> None:
    print("=" * 55)
    print("  EVAL HARNESS v3 — Multi-Metric RAG Evaluation")
    print("=" * 55)
    print(f"  Timestamp : {report['timestamp']}")
    print(f"  Total     : {report['total']}")
    print(f"  Passed    : {report['passed']}")
    print(f"  Failed    : {report['failed']}")
    print(f"  Pass Rate : {report['pass_rate']}")
    print("-" * 55)

    for r in report["results"]:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"\n  [{status}] {r['case_name']}")
        print(f"    keyword_score   : {r['keyword_score']}")
        print(f"    citation_ok     : {r['citation_ok']}")
        print(f"    faithfulness_ok : {r['faithfulness_ok']}")
        print(f"    relevance_ok    : {r['relevance_ok']}")
        print(f"    length_ok       : {r['length_ok']}")
        print(f"    no_answer_ok    : {r['no_answer_correct']}")
        if not r["passed"]:
            print(f"    FAIL REASONS    : {'; '.join(r['failure_reasons'])}")

    print("\n" + "=" * 55)


# ── Test Cases ────────────────────────────────────────────────────

def get_test_cases() -> List[EvalCase]:
    return [
        EvalCase(
            name="rag_definition",
            question="What is RAG?",
            expected_keywords=["retrieval", "augmented", "generation"],
            expected_citations=["doc_rag_intro.md"],
            source_context="RAG is Retrieval Augmented Generation. It fetches documents before answering.",
            min_keyword_score=0.66,
        ),
        EvalCase(
            name="chunking_reason",
            question="Why chunking matters?",
            expected_keywords=["retrieval", "precision", "chunking"],
            expected_citations=["doc_chunking_notes.md"],
            source_context="Chunking splits docs into smaller pieces for better retrieval precision.",
            min_keyword_score=0.5,
        ),
        EvalCase(
            name="hallucination_control",
            question="What is hallucination control?",
            expected_keywords=["grounding", "citations", "reduces"],
            expected_citations=["doc_reliability.md"],
            source_context="Hallucination control uses grounding and citations to reduce false claims.",
            min_keyword_score=0.5,
        ),
        # ADVERSARIAL: off-topic question (should still pass relevance)
        EvalCase(
            name="off_topic_france",
            question="What is the capital of France?",
            expected_keywords=["paris", "capital"],
            expected_citations=[],
            source_context="France is a country in Europe. Its capital is Paris.",
            min_keyword_score=0.5,
        ),
        # ADVERSARIAL: unanswerable question (model should say "I don't know")
        EvalCase(
            name="unanswerable_unicorn",
            question="What is the unicorn population of Mars?",
            expected_keywords=[],
            expected_citations=[],
            source_context="No relevant information found.",
            is_unanswerable=True,
        ),
        # ADVERSARIAL: answerable but model will fail (no answer in bank)
        EvalCase(
            name="edge_case_empty",
            question="Explain quantum entanglement in RAG systems.",
            expected_keywords=["quantum"],
            expected_citations=["doc_quantum.md"],
            source_context="Quantum computing is not related to RAG systems.",
            min_keyword_score=0.5,
        ),
    ]


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    cases = get_test_cases()
    report = run_suite(cases)
    print_report(report)

    # Save JSON report
    out_path = "eval_results_v3.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report saved to: {out_path}")
