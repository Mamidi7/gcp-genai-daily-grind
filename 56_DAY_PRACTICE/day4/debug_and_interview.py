"""
Day 4 — Debug Cards + Interview Answers for Production OOP Examples
Run: python -c "import debug_and_interview"
"""

# ═══════════════════════════════════════════════════════════════════════════════
# DEBUG CARD 1: Mutable Default Arguments
# ═══════════════════════════════════════════════════════════════════════════════

SYMPTOM = """
validator1 = TransactionValidator()
validator2 = TransactionValidator()
# Modify validator1's rules
validator1.rules['min_amount'] = 100
# validator2's rules ALSO changed! Both share the SAME dict object.
"""

ROOT_CAUSE = """
Python evaluates default arguments ONCE at function definition time.
If the default is a MUTABLE object (list, dict, set), ALL instances
share the SAME object. Changing it in one instance changes it everywhere.
"""

FIX = """
def __init__(self, rules: dict | None = None):
    self.rules = rules if rules is not None else {
        "min_amount": 0.01,
        ...
    }
# This creates a NEW dict every time __init__ runs.
"""

PREVENTION = """
RULE: Never use mutable objects as default arguments.
Always use None + conditional assignment.
Pydantic handles this automatically with Field(default_factory=...).
"""

IMPACT = """
In production: If two batch processors share the same config object silently,
one batch might use wrong validation rules without anyone noticing.
This is a HARD bug to find because it only happens at runtime with
specific instance creation ordering.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DEBUG CARD 2: TypeError on Missing Keys (Fail-Fast)
# ═══════════════════════════════════════════════════════════════════════════════

SYMPTOM_2 = """
cfg = ConfigManager()  # If PROJECT_ID not set in env
# → ValueError: Missing required config: ['PROJECT_ID']
"""

ROOT_CAUSE_2 = """
No explicit problem — this is INTENTIONAL fail-fast behavior.
But a common mistake is catching the error too late (mid-request)
instead of at startup.
"""

FIX_2 = """
# WRONG: validate mid-request
@app.post("/generate")
async def generate():
    project = os.environ.get("PROJECT_ID")  # might fail HERE
    ...

# RIGHT: validate at startup
cfg = ConfigManager()  # fails IMMEDIATELY if config is wrong
app.state.cfg = cfg
"""

PREVENTION_2 = """
Always validate configuration at MODULE LOAD TIME, not request time.
This way the service fails to START instead of failing mid-request
(a 503 is better than a corrupted response).
"""

IMPACT_2 = """
At a bank: If a config change causes wrong project ID mid-batch,
you could write to the wrong environment (prod vs dev).
Failing at startup prevents this entirely.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DEBUG CARD 3: Partial Batch Failures (Aggregation Pattern)
# ═══════════════════════════════════════════════════════════════════════════════

SYMPTOM_3 = """
BatchProcessor processes 10,000 records. 3 fail validation.
Without aggregation, the entire batch is rejected.
With aggregation, only the 3 bad records are rejected,
but 9,997 are processed successfully.
"""

ROOT_CAUSE_3 = """
ETL pipelines often treat any failure as total failure.
But in production, partial processing with error logging
is preferred — reject only what's bad, keep what's good.
"""

FIX_3 = """
Use ProcessingResult to collect per-record errors:
- processed: list of valid records
- errors: list of {index, record_id, validation_errors}
- pass_rate: percentage passed
"""

PREVENTION_3 = """
Design batch processing to isolate failures per record.
Log each failure with enough context to debug.
Never silently skip — always count and report.
"""

IMPACT_3 = """
In banking ETL: If 3 out of 10,000 transactions fail,
you don't want to halt all 10,000. Process the good ones,
log the bad ones with their errors, and send an alert.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW ANSWER 1: 30-Second — TransactionValidator
# ═══════════════════════════════════════════════════════════════════════════════

INTERVIEW_30S = """
"I use validator classes to check data before processing. In my ETL pipeline,
TransactionValidator validates amounts, currencies, and account IDs before
any record is processed. If validation fails, the error is collected and logged
but the good records still pass through. This prevents bad data from corrupting
downstream systems without stopping the entire pipeline."
"""

# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW ANSWER 2: 90-Second STAR — ProcessingResult + Error Tracking
# ═══════════════════════════════════════════════════════════════════════════════

INTERVIEW_90S_STAR = """
SITUATION: In my banking ETL pipeline, we processed 10,000+ transactions
daily. Any validation failure would reject the entire batch, requiring
manual re-processing.

TASK: I needed to design a system that processes valid records while
collecting detailed errors on failed ones — without blocking the good data.

ACTION: I built a BatchProcessor that wraps a TransactionValidator.
Each record is validated independently. Valid records go to processing.
Failed records go to an error collection with: record ID, field that failed,
and the expected vs actual value. At the end, a ProcessingResult shows:
total, passed, failed, and pass rate.

RESULT: Pass rate improved from all-or-nothing to 99.97% throughput.
Failed records were tracked in BigQuery with enough detail to debug.
The error collection was later used to build a dashboard showing
top failure reasons per batch.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW ANSWER 3: 3-Minute Walkthrough — Full OOP Design
# ═══════════════════════════════════════════════════════════════════════════════

INTERVIEW_3MIN = """
"The key OOP concepts I use daily in production are:

1. ENCAPSULATION (TransactionValidator):
   The validator wraps validation rules AND error collection together.
   Callers don't know how validation works — they just call .validate()
   and check the return value. This hides complexity and makes the
   interface simple.

2. COMPOSITION (BatchProcessor has-a TransactionValidator):
   Instead of duplicating validation logic, BatchProcessor reuses
   TransactionValidator. This is 'favor composition over inheritance' —
   the processor doesn't IS-A validator, it HAS-A validator.
   This lets me swap validators without changing the processor.

3. INHERITANCE (ErrorResponse extends APIResponse):
   APIResponse provides the base contract (success, data, message).
   ErrorResponse extends it with error_code, details, status_code.
   Both can be passed to any function expecting APIResponse because
   they share the .to_dict() interface. This is polymorphism.

4. FACTORY PATTERN (ConfigManager.from_dict / from_file / from_env):
   Different environments need different config loading strategies.
   Instead of if/else in the caller, I provide class methods that
   return configured instances. The caller just says 'I need config'
   without knowing how it's loaded.

The common thread: Each pattern solves a real production problem
I encountered in ETL pipelines — not textbook theory."
"""

# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW CONVERSION: How to talk about this
# ═══════════════════════════════════════════════════════════════════════════════

HOW_TO_TALK = """
30-SECOND PITCH:
"I built production-style Python classes for my ETL pipeline:
TransactionValidator for data quality checks, BatchProcessor
with per-record error tracking, and standardized API response
objects for my FastAPI endpoints. Each follows OOP patterns
that prevent entire class of bugs I've hit in real ETL work."

90-SECOND STAR (use when asked about data quality):
"If asked about error handling — tell the ProcessingResult story.
It shows you think about partial failures, error tracking,
and observability. All rare in AI engineers."

3-MINUTE DEEP DIVE (use when asked about design choices):
"Walk through all 4 patterns and WHY each was chosen.
The interviewer wants to hear: you don't just use OOP,
you understand WHEN each pattern fits."
"""


if __name__ == "__main__":
    print("=" * 60)
    print("DEBUG CARDS + INTERVIEW ANSWERS")
    print("=" * 60)
    print("\n--- Debug Card 1: Mutable Defaults ---")
    print(SYMPTOM)
    print("Root cause:", ROOT_CAUSE.strip()[:80])
    print("Fix: Use None + conditional")
    print("Prevention: Never use mutable defaults")

    print("\n--- Debug Card 2: Fail-Fast Config ---")
    print(SYMPTOM_2)
    print("Root cause:", ROOT_CAUSE_2.strip()[:80])

    print("\n--- Debug Card 3: Partial Batch Failures ---")
    print(SYMPTOM_3)
    print("Root cause:", ROOT_CAUSE_3.strip()[:80])

    print("\n--- Interview Answers ---")
    print("\n30-SECOND:")
    print(INTERVIEW_30S.strip())
    print("\n90-SECOND STAR:")
    print(INTERVIEW_90S_STAR.strip())
    print("\n3-MINUTE:")
    print(INTERVIEW_3MIN.strip())
    print("\n--- End of Interview Answers ---")
