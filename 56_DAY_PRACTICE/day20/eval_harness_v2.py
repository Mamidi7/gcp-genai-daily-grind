"""
Day 20 - Eval Harness v2
Goal: measurable evaluation artifact for RAG-style answers.
Run: python eval_harness_v2.py
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EvalCase:
    name: str
    question: str
    expected_keywords: List[str]
    expected_citations: List[str]
    min_keyword_score: float = 0.6


@dataclass
class EvalResult:
    case_name: str
    passed: bool
    keyword_score: float
    citation_ok: bool
    failure_reason: str


def keyword_score(answer: str, keywords: List[str]) -> float:
    if not keywords:
        return 1.0
    ans = answer.lower()
    hit = sum(1 for k in keywords if k.lower() in ans)
    return hit / len(keywords)


def citation_ok(answer: str, citations: List[str]) -> bool:
    ans = answer.lower()
    return any(c.lower() in ans for c in citations)


def evaluate_one(case: EvalCase, answer: str) -> EvalResult:
    k_score = keyword_score(answer, case.expected_keywords)
    c_ok = citation_ok(answer, case.expected_citations)
    passed = k_score >= case.min_keyword_score and c_ok

    reason = ""
    if not passed:
        if k_score < case.min_keyword_score:
            reason += f"low keyword score ({k_score:.2f}); "
        if not c_ok:
            reason += "missing citation;"

    return EvalResult(
        case_name=case.name,
        passed=passed,
        keyword_score=round(k_score, 2),
        citation_ok=c_ok,
        failure_reason=reason.strip() or "-",
    )


def fake_rag_answer(question: str) -> str:
    # Replace with real model call later.
    bank = {
        "What is RAG?": "RAG means retrieval augmented generation. It retrieves context before generation. Source: doc_rag_intro.md",
        "Why chunking matters?": "Chunking helps retrieval precision and context boundaries. Source: doc_chunking_notes.md",
        "What is hallucination control?": "Use grounding and citations to reduce unsupported claims. Source: doc_reliability.md",
    }
    return bank.get(question, "I do not know. Source: unknown")


def run_suite(cases: List[EvalCase]) -> Dict:
    results = []
    for case in cases:
        ans = fake_rag_answer(case.question)
        results.append(evaluate_one(case, ans))

    total = len(results)
    passed = sum(1 for r in results if r.passed)

    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 2) if total else 0.0,
        "results": results,
    }


def print_report(report: Dict) -> None:
    print("=== Eval Harness v2 Report ===")
    print(f"Total: {report['total']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")
    print(f"Pass Rate: {report['pass_rate']}")
    print("--- Details ---")
    for r in report["results"]:
        print(
            f"{r.case_name}: passed={r.passed}, keyword_score={r.keyword_score}, citation_ok={r.citation_ok}, reason={r.failure_reason}"
        )


if __name__ == "__main__":
    CASES = [
        EvalCase(
            name="rag_definition",
            question="What is RAG?",
            expected_keywords=["retrieval", "augmented", "generation"],
            expected_citations=["doc_rag_intro.md"],
            min_keyword_score=0.66,
        ),
        EvalCase(
            name="chunking_reason",
            question="Why chunking matters?",
            expected_keywords=["retrieval", "precision", "context"],
            expected_citations=["doc_chunking_notes.md"],
            min_keyword_score=0.66,
        ),
        EvalCase(
            name="hallucination_control",
            question="What is hallucination control?",
            expected_keywords=["grounding", "citations", "reduce"],
            expected_citations=["doc_reliability.md"],
            min_keyword_score=0.66,
        ),
    ]

    report = run_suite(CASES)
    print_report(report)
