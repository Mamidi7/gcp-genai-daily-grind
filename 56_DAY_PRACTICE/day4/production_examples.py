"""
Day 4 — Production OOP Examples
Replace rote Document/DocumentChunk with real-world patterns.
Each example = one OOP concept + debug story + interview answer.

Run: python production_examples.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: TransactionValidator — Basic Class + Validation
# ═══════════════════════════════════════════════════════════════════════════════
# Real use: In ETL pipelines, validate each row before processing.
# Interview angle: "How do you validate data before processing?"


class TransactionValidator:
    """Validates banking/ETL transaction records.

    Production note: In banking ETL, a single bad record can break
    an entire batch. Validate BEFORE processing.
    """

    def __init__(self, rules: dict | None = None):
        # COMMON MISTAKE: mutable default arg like rules={}
        # Using None + conditional avoids shared-state bugs
        self.rules = rules if rules is not None else {
            "min_amount": 0.01,
            "max_amount": 1_000_000,
            "allowed_currencies": ["USD", "EUR", "INR", "GBP"],
        }
        self.errors: list[str] = []

    def validate(self, transaction: dict) -> bool:
        """Returns True if valid. Collects errors in self.errors."""
        self.errors.clear()

        amount = transaction.get("amount", 0)
        if amount < self.rules["min_amount"]:
            self.errors.append(f"amount {amount} below min {self.rules['min_amount']}")
        if amount > self.rules["max_amount"]:
            self.errors.append(f"amount {amount} exceeds max {self.rules['max_amount']}")

        currency = transaction.get("currency", "")
        if currency not in self.rules["allowed_currencies"]:
            self.errors.append(f"currency '{currency}' not in {self.rules['allowed_currencies']}")

        if not transaction.get("account_id"):
            self.errors.append("missing account_id")

        return len(self.errors) == 0

    def validate_batch(self, transactions: list[dict]) -> list[dict]:
        """Validate many, return only the valid ones. Invalid go to errors log."""
        valid = []
        for txn in transactions:
            if self.validate(txn):
                valid.append(txn)
            else:
                # In production: log to BigQuery error table
                print(f"  [REJECTED] {txn.get('id', '?')}: {self.errors}")
        return valid


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: BatchProcessor — Aggregation + Error Tracking
# ═══════════════════════════════════════════════════════════════════════════════
# Real use: Process batches with per-record error tracking.
# Shows: composition (has-a validator), result objects, pass rate.


class ProcessingResult:
    """Holds batch processing summary. Immutable after creation."""

    def __init__(self, total: int, passed: int, failed: int, errors: list[dict]):
        self.total = total
        self.passed = passed
        self.failed = failed
        self.errors = errors
        self.pass_rate = round(passed / total * 100, 2) if total > 0 else 0.0

    def summary(self) -> str:
        return (f"Batch: {self.total} records | "
                f"✅ {self.passed} passed | "
                f"❌ {self.failed} failed | "
                f"📊 {self.pass_rate}% pass rate")


class BatchProcessor:
    """Processes batch of records. Composes a validator internally.

    Production pattern: One processor, pluggable validator.
    """

    def __init__(self, validator: TransactionValidator):
        self.validator = validator
        self.processed: list[dict] = []

    def run(self, records: list[dict]) -> ProcessingResult:
        self.processed = []
        errors: list[dict] = []

        for i, record in enumerate(records):
            if self.validator.validate(record):
                self.processed.append(record)
            else:
                errors.append({
                    "index": i,
                    "record_id": record.get("id", "unknown"),
                    "validation_errors": list(self.validator.errors),
                })

        return ProcessingResult(
            total=len(records),
            passed=len(self.processed),
            failed=len(errors),
            errors=errors,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: APIResponse + ErrorResponse — Inheritance
# ═══════════════════════════════════════════════════════════════════════════════
# Real use: Every FastAPI endpoint returns standardized responses.
# Shows: super().__init__(), method override, extending parent.


class APIResponse:
    """Standard response envelope. Every endpoint returns this shape."""

    def __init__(self, success: bool, data=None, message: str = ""):
        self.success = success
        self.data = data
        self.message = message

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
        }

    def __repr__(self) -> str:
        return f"APIResponse(success={self.success}, has_data={self.data is not None})"


class ErrorResponse(APIResponse):
    """Extends APIResponse with machine-readable error codes.

    Real use: Catch-all exception handler returns structured errors.
    """

    def __init__(self, message: str, error_code: str, details: dict | None = None,
                 status_code: int = 400):
        super().__init__(success=False, data=None, message=message)
        self.error_code = error_code
        self.details = details if details is not None else {}
        self.status_code = status_code

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["error_code"] = self.error_code
        base["details"] = self.details
        base["status_code"] = self.status_code
        return base


class SuccessResponse(APIResponse):
    """Convenience wrapper for success responses."""

    def __init__(self, data=None, message: str = "ok"):
        super().__init__(success=True, data=data, message=message)


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: ConfigManager — Factory Pattern + Environment Resolution
# ═══════════════════════════════════════════════════════════════════════════════
# Real use: Service config that works locally AND in Cloud Run.
# Shows: @classmethod factory, validation at construction, fail-fast.


class ConfigManager:
    """Loads config from env vars or file. Fails fast on missing keys.

    Production pattern: Validate ALL config at startup, not mid-request.
    """

    REQUIRED_KEYS = {
        "PROJECT_ID": str,
        "LOCATION": str,
        "MODEL_ID": str,
    }
    OPTIONAL_KEYS = {
        "TEMPERATURE": float,
        "MAX_TOKENS": int,
    }

    def __init__(self, source: str = "env"):
        self.source = source
        self._config: dict[str, str | int | float] = {}
        self._load()

    def _load(self) -> None:
        """Load config from env vars. Fail fast if required keys missing."""
        missing = []
        for key, expected_type in self.REQUIRED_KEYS.items():
            raw = os.environ.get(key)
            if raw is None:
                missing.append(key)
            else:
                self._config[key] = self._cast(raw, expected_type, key)

        if missing:
            raise ValueError(
                f"Missing required config: {missing}. "
                f"Set them as env vars or use ConfigManager.from_file()."
            )

        for key, expected_type in self.OPTIONAL_KEYS.items():
            raw = os.environ.get(key)
            if raw is not None:
                self._config[key] = self._cast(raw, expected_type, key)

    def _cast(self, raw: str, expected_type: type, key: str):
        """Cast string env var to expected type. Fail on bad format."""
        try:
            if expected_type == int:
                return int(raw)
            elif expected_type == float:
                return float(raw)
            return raw
        except ValueError:
            raise ValueError(
                f"Config '{key}' = '{raw}' cannot be cast to {expected_type.__name__}"
            )

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    @classmethod
    def from_file(cls, path: str = "config.json") -> "ConfigManager":
        """Alternative factory: load from JSON file (local dev)."""
        instance = cls.__new__(cls)  # skip __init__
        instance.source = "file"
        instance._config = {}
        # Actually load from file
        import json
        from pathlib import Path
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        data = json.loads(file_path.read_text())
        missing = [k for k in cls.REQUIRED_KEYS if k not in data]
        if missing:
            raise ValueError(f"Missing required keys in {path}: {missing}")
        instance._config = data
        return instance

    @classmethod
    def from_dict(cls, config: dict) -> "ConfigManager":
        """Alternative factory: from dict (for testing)."""
        missing = [k for k in cls.REQUIRED_KEYS if k not in config]
        if missing:
            raise ValueError(f"Missing required keys: {missing}")
        instance = cls.__new__(cls)
        instance.source = "test"
        instance._config = dict(config)
        return instance


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════════════════════

import os


def test_transaction_validator():
    print("\n=== Test: TransactionValidator ===")

    v = TransactionValidator()

    # Happy path
    txn = {"id": "T1", "account_id": "ACC123", "amount": 500.0, "currency": "USD"}
    assert v.validate(txn), "Valid txn should pass"
    print("  ✅ Valid transaction passes")

    # Invalid amount
    txn2 = {"id": "T2", "account_id": "ACC456", "amount": -5, "currency": "USD"}
    assert not v.validate(txn2), "Negative amount should fail"
    print(f"  ✅ Negative amount rejected: {v.errors}")

    # Invalid currency
    txn3 = {"id": "T3", "account_id": "ACC789", "amount": 100, "currency": "XYZ"}
    assert not v.validate(txn3), "Bad currency should fail"
    print(f"  ✅ Bad currency rejected: {v.errors}")

    # Missing account_id
    txn4 = {"id": "T4", "amount": 100, "currency": "USD"}
    assert not v.validate(txn4), "Missing account_id should fail"
    print(f"  ✅ Missing account_id rejected: {v.errors}")

    # Batch validation
    batch = [txn, txn2, txn3, txn4]
    valid = v.validate_batch(batch)
    assert len(valid) == 1, "Only 1 should pass"
    print(f"  ✅ Batch: {len(valid)} valid out of {len(batch)}")


def test_batch_processor():
    print("\n=== Test: BatchProcessor ===")

    v = TransactionValidator()
    bp = BatchProcessor(v)

    records = [
        {"id": "R1", "account_id": "A1", "amount": 100, "currency": "USD"},
        {"id": "R2", "account_id": "A2", "amount": -10, "currency": "USD"},
        {"id": "R3", "account_id": "A3", "amount": 200, "currency": "EUR"},
        {"id": "R4", "account_id": "", "amount": 50, "currency": "INR"},
    ]

    result = bp.run(records)

    assert result.total == 4
    assert result.passed == 2   # R1, R3
    assert result.failed == 2   # R2, R4
    assert result.pass_rate == 50.0
    assert len(result.errors) == 2

    print(f"  ✅ {result.summary()}")
    for err in result.errors:
        print(f"     Failed: {err['record_id']} — {err['validation_errors']}")


def test_api_responses():
    print("\n=== Test: APIResponse Inheritance ===")

    # Base response
    r1 = APIResponse(success=True, data={"user": "krishna"}, message="login ok")
    d1 = r1.to_dict()
    assert d1["success"] is True
    assert d1["data"]["user"] == "krishna"
    print(f"  ✅ APIResponse: {d1}")

    # Error response (inherits + extends)
    err = ErrorResponse(
        message="Invalid credentials",
        error_code="AUTH_001",
        details={"failed_attempts": 3},
        status_code=401,
    )
    d2 = err.to_dict()
    assert d2["success"] is False
    assert d2["error_code"] == "AUTH_001"
    assert d2["status_code"] == 401
    assert d2["data"] is None
    print(f"  ✅ ErrorResponse: {d2}")

    # SuccessResponse convenience
    s = SuccessResponse(data={"result": "done"})
    assert s.success is True
    assert s.message == "ok"
    print(f"  ✅ SuccessResponse: {s.to_dict()}")

    # Polymorphism: both share .to_dict()
    responses: list[APIResponse] = [r1, err, s]
    for r in responses:
        assert hasattr(r, "to_dict"), "All responses must have to_dict"
        assert callable(r.to_dict)
    print(f"  ✅ Polymorphism: all {len(responses)} response types share to_dict()")


def test_config_manager():
    print("\n=== Test: ConfigManager ===")

    # Test from_dict (test-friendly)
    cfg = ConfigManager.from_dict({
        "PROJECT_ID": "my-project",
        "LOCATION": "us-central1",
        "MODEL_ID": "gemini-2.0-flash",
    })

    assert cfg.get("PROJECT_ID") == "my-project"
    assert cfg.get("LOCATION") == "us-central1"
    assert cfg.get("NONEXISTENT") is None
    print(f"  ✅ ConfigManager.from_dict works")

    # Test missing required key fails fast
    try:
        ConfigManager.from_dict({"PROJECT_ID": "my-project"})  # missing LOCATION, MODEL_ID
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "LOCATION" in str(e)
        print(f"  ✅ Missing key fails fast: {e}")

    # Test from_file fails gracefully
    try:
        ConfigManager.from_file("nonexistent.json")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"  ✅ Missing file fails fast: {e}")


def run_all():
    print("=" * 60)
    print("DAY 4 — PRODUCTION OOP EXAMPLES")
    print("=" * 60)
    print("""
  Example 1: TransactionValidator  → Basic class + validation
  Example 2: BatchProcessor         → Aggregation + error tracking
  Example 3: APIResponse/Error      → Inheritance + polymorphism
  Example 4: ConfigManager          → Factory pattern + fail-fast
    """)

    test_transaction_validator()
    test_batch_processor()
    test_api_responses()
    test_config_manager()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)


if __name__ == "__main__":
    run_all()
