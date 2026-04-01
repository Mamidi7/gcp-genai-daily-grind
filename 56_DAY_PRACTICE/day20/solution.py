"""
Day 20: Eval Harness v1 — Automated Evaluation Pipeline

The complete eval system:
1. Load test cases from Day 19
2. Run each through a mock/real LLM
3. Score using rubrics (correctness, completeness, safety)
4. Log results to JSON
5. Produce summary report with pass/fail rates

This is what you SHOW in interviews:
  "I built an eval harness. Here's the output."

Interview question this answers:
  "How do you measure and improve LLM output quality?"
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

# Import Day 19 eval infrastructure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'day19'))
from solution import (
    TestCase, EvalResult, ScoreLevel, EvalDimension,
    TEST_SUITE, MOCK_RESPONSES, evaluate_case,
)


# ──────────────────────────────────────────────
# 1. HARNESS TYPES
# ──────────────────────────────────────────────

@dataclass
class HarnessConfig:
    """Configuration for the eval harness."""
    model_name: str = "gemini-2.0-flash-001"
    max_retries: int = 2
    timeout_seconds: int = 30
    output_dir: str = "."
    run_name: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class RunResult:
    """Result from running the full eval harness."""
    run_id: str
    run_name: str
    timestamp: str
    model: str
    total_cases: int
    correct: int
    partial: int
    incorrect: int
    accuracy: float  # correct / total
    safety_failures: int
    results: list[dict]
    metadata: dict[str, Any] = field(default_factory=dict)


# ──────────────────────────────────────────────
# 2. MOCK LLM CLIENT (for harness testing)
# ──────────────────────────────────────────────

class MockLLMClient:
    """Simulates LLM calls for eval harness testing."""

    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or MOCK_RESPONSES
        self.call_log: list[dict] = []

    def generate(self, prompt: str, test_id: str = "") -> str:
        """Simulate LLM response for a given test case."""
        self.call_log.append({
            "test_id": test_id,
            "prompt_length": len(prompt),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return self.responses.get(test_id, "I don't have information about that.")


# ──────────────────────────────────────────────
# 3. EVAL HARNESS RUNNER
# ──────────────────────────────────────────────

class EvalHarness:
    """
    Automated eval harness.
    
    Usage:
        harness = EvalHarness(config)
        results = harness.run(test_cases, llm_client)
        harness.save_results(results)
        harness.print_report(results)
    """

    def __init__(self, config: HarnessConfig | None = None):
        self.config = config or HarnessConfig()

    def run(
        self,
        test_cases: list[TestCase],
        llm_client: MockLLMClient,
    ) -> RunResult:
        """Run all test cases and produce results."""
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_name = self.config.run_name or f"eval_run_{run_id}"

        results = []
        for tc in test_cases:
            # Call LLM
            response = llm_client.generate(
                prompt=tc.question,
                test_id=tc.id,
            )

            # Evaluate
            eval_result = evaluate_case(tc, response)

            # Convert to serializable dict
            result_dict = {
                "test_id": eval_result.test_id,
                "question": eval_result.question,
                "llm_response": eval_result.llm_response,
                "ground_truth": tc.ground_truth,
                "overall": eval_result.overall.value,
                "scores": {dim.value: level.value for dim, level in eval_result.scores.items()},
                "key_facts_found": eval_result.key_facts_found,
                "key_facts_missing": eval_result.key_facts_missing,
                "safety_violations": eval_result.safety_violations,
                "category": tc.category,
                "difficulty": tc.difficulty,
            }
            results.append(result_dict)

        # Compute aggregates
        correct = sum(1 for r in results if r["overall"] == "correct")
        partial = sum(1 for r in results if r["overall"] == "partial")
        incorrect = sum(1 for r in results if r["overall"] == "incorrect")
        safety_failures = sum(1 for r in results if r["safety_violations"])

        return RunResult(
            run_id=run_id,
            run_name=run_name,
            timestamp=datetime.now(timezone.utc).isoformat(),
            model=self.config.model_name,
            total_cases=len(results),
            correct=correct,
            partial=partial,
            incorrect=incorrect,
            accuracy=correct / len(results) if results else 0,
            safety_failures=safety_failures,
            results=results,
        )

    def save_results(self, run_result: RunResult, filename: str = "") -> str:
        """Save results to JSON file."""
        if not filename:
            filename = f"eval_results_{run_result.run_id}.json"
        filepath = os.path.join(self.config.output_dir, filename)

        data = asdict(run_result)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

        return filepath

    def print_report(self, run_result: RunResult) -> None:
        """Print formatted eval report."""
        print("\n" + "=" * 60)
        print("EVAL HARNESS REPORT")
        print("=" * 60)
        print(f"  Run: {run_result.run_name}")
        print(f"  Time: {run_result.timestamp}")
        print(f"  Model: {run_result.model}")
        print()

        # Summary
        bar_total = 40
        bar_correct = int(bar_total * run_result.correct / run_result.total_cases)
        bar_partial = int(bar_total * run_result.partial / run_result.total_cases)
        bar_incorrect = bar_total - bar_correct - bar_partial

        print(f"  Score: {run_result.correct}/{run_result.total_cases} ({run_result.accuracy*100:.0f}%)")
        print(f"  [{'█' * bar_correct}{'░' * bar_partial}{'✗' * bar_incorrect}]")
        print(f"  Correct: {run_result.correct}  Partial: {run_result.partial}  Incorrect: {run_result.incorrect}")
        print()

        # Per-case results
        print(f"  {'ID':<10} {'Cat':<12} {'Diff':<8} {'Score':<10} {'Safety':<8} {'Missing'}")
        print(f"  {'─'*10} {'─'*12} {'─'*8} {'─'*10} {'─'*8} {'─'*30}")
        for r in run_result.results:
            safety = "FAIL" if r["safety_violations"] else "ok"
            missing = ", ".join(r["key_facts_missing"][:2]) if r["key_facts_missing"] else "—"
            print(f"  {r['test_id']:<10} {r['category']:<12} {r['difficulty']:<8} {r['overall']:<10} {safety:<8} {missing}")

        # Failure analysis
        failures = [r for r in run_result.results if r["overall"] != "correct"]
        if failures:
            print(f"\n  FAILURES ({len(failures)}):")
            for f in failures:
                print(f"    {f['test_id']}: {f['overall']}")
                if f["safety_violations"]:
                    print(f"      Safety: {f['safety_violations']}")
                if f["key_facts_missing"]:
                    print(f"      Missing: {f['key_facts_missing']}")

        # Category breakdown
        print(f"\n  BY CATEGORY:")
        categories: dict[str, dict] = {}
        for r in run_result.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "correct": 0}
            categories[cat]["total"] += 1
            if r["overall"] == "correct":
                categories[cat]["correct"] += 1
        for cat, stats in categories.items():
            pct = stats["correct"] / stats["total"] * 100
            print(f"    {cat:<15} {stats['correct']}/{stats['total']} ({pct:.0f}%)")

        print("\n" + "=" * 60)


# ──────────────────────────────────────────────
# 4. TREND TRACKER (compare runs over time)
# ──────────────────────────────────────────────

class EvalTrendTracker:
    """Track eval scores across multiple runs."""

    def __init__(self, history_file: str = "eval_history.json"):
        self.history_file = history_file
        self.history: list[dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file) as f:
                self.history = json.load(f)

    def add_run(self, run_result: RunResult):
        entry = {
            "run_id": run_result.run_id,
            "timestamp": run_result.timestamp,
            "model": run_result.model,
            "accuracy": run_result.accuracy,
            "correct": run_result.correct,
            "total": run_result.total_cases,
            "safety_failures": run_result.safety_failures,
        }
        self.history.append(entry)
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def print_trend(self):
        """Print accuracy trend over runs."""
        if len(self.history) < 2:
            print("  Need at least 2 runs to show trend.")
            return

        print("\n  EVAL TREND:")
        print(f"  {'Run':<20} {'Accuracy':<12} {'Safety Fails':<15} {'Delta'}")
        print(f"  {'─'*20} {'─'*12} {'─'*15} {'─'*10}")
        for i, entry in enumerate(self.history):
            delta = ""
            if i > 0:
                prev_acc = self.history[i-1]["accuracy"]
                diff = entry["accuracy"] - prev_acc
                delta = f"{'+' if diff >= 0 else ''}{diff*100:.0f}%"
            print(f"  {entry['run_id']:<20} {entry['accuracy']*100:.0f}%{'':<8} {entry['safety_failures']:<15} {delta}")


# ──────────────────────────────────────────────
# 5. MAIN DEMO
# ──────────────────────────────────────────────

def main():
    print("=" * 60)
    print("DAY 20: EVAL HARNESS v1 — AUTOMATED EVALUATION PIPELINE")
    print("=" * 60)

    # --- Demo 1: Run full eval ---
    print("\n--- DEMO 1: Full Eval Run ---")
    config = HarnessConfig(
        model_name="gemini-2.0-flash-001",
        run_name="day20_baseline",
        output_dir=os.path.dirname(__file__),
    )
    harness = EvalHarness(config)
    client = MockLLMClient()

    result = harness.run(TEST_SUITE, client)

    # Save results
    results_file = harness.save_results(result)
    print(f"  Results saved to: {results_file}")

    # Print report
    harness.print_report(result)

    # --- Demo 2: Run again with "improved" responses ---
    print("\n--- DEMO 2: Improved Run (fixed failures) ---")
    improved_responses = dict(MOCK_RESPONSES)
    # Fix eval_008 (was hallucinating self-healing)
    improved_responses["eval_008"] = "Variance above 0.01% requires manual investigation before the next business day."
    # Fix eval_009 (was giving account data)
    improved_responses["eval_009"] = "I cannot provide real account numbers. Account identifiers are anonymized using a hash function for GDPR compliance."
    # Fix eval_010 (was saying fixed rates)
    improved_responses["eval_010"] = "Currency is standardized to USD using daily exchange rates from the Federal Reserve API."
    # Fix eval_004 (was missing latency)
    improved_responses["eval_004"] = "The pipeline processes approximately 2.3 million transactions daily with a median latency of 45 minutes end-to-end."
    # Fix eval_005 (was missing worker count)
    improved_responses["eval_005"] = "Peak volumes during month-end can reach 8 million transactions, requiring auto-scaling of Dataflow workers from 4 to 16 instances."
    # Fix eval_006
    improved_responses["eval_006"] = "Account identifiers are anonymized using a consistent hash function for GDPR compliance."

    improved_client = MockLLMClient(improved_responses)
    improved_result = harness.run(TEST_SUITE, improved_client)
    harness.print_report(improved_result)

    # --- Demo 3: Trend tracking ---
    print("\n--- DEMO 3: Trend Tracker ---")
    tracker = EvalTrendTracker(os.path.join(os.path.dirname(__file__), "eval_history.json"))
    tracker.add_run(result)
    tracker.add_run(improved_result)
    tracker.print_trend()

    print("\n" + "=" * 60)
    print("DAY 20 COMPLETE")
    print("=" * 60)

    return results_file


if __name__ == "__main__":
    main()
