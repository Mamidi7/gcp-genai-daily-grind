"""Day 15: Provider-agnostic LLM gateway wrapper with structured output."""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from dataclasses import dataclass
from typing import Protocol


class ParseError(Exception):
    pass


class GatewayTimeoutError(Exception):
    pass


class UpstreamError(Exception):
    pass


class LLMClient(Protocol):
    async def generate(self, prompt: str) -> str:  # raw JSON text expected
        ...


@dataclass
class WrapperResponse:
    answer: str
    confidence: float
    source: str
    request_id: str
    latency_ms: float
    provider: str
    model: str

    def to_log_fields(self) -> dict[str, str | float]:
        """Small observability hook for request tracing and dashboards."""
        return {
            "request_id": self.request_id,
            "latency_ms": self.latency_ms,
            "provider": self.provider,
            "model": self.model,
            "confidence": self.confidence,
            "source": self.source,
        }


class SimpleLLMWrapper:
    """Single boundary between app code and provider SDK."""

    def __init__(
        self,
        client: LLMClient,
        timeout_s: float = 8.0,
        max_retries: int = 2,
        provider: str = "fake-provider",
        model: str = "fake-model",
    ):
        self.client = client
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.provider = provider
        self.model = model

    async def ask(self, prompt: str) -> WrapperResponse:
        request_id = str(uuid.uuid4())
        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            started_at = time.perf_counter()
            try:
                raw = await asyncio.wait_for(self.client.generate(prompt), timeout=self.timeout_s)
                latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
                return self._parse(raw, request_id=request_id, latency_ms=latency_ms)
            except ParseError:
                raise
            except asyncio.TimeoutError as exc:
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.2 * (attempt + 1))
                    continue
                raise GatewayTimeoutError(f"LLM timed out after retries: {request_id}") from exc
            except Exception as exc:  # timeout / transient upstream errors
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.2 * (attempt + 1))
                    continue
                break

        raise UpstreamError(f"LLM call failed after retries: {last_error}")

    def _parse(self, raw: str, *, request_id: str, latency_ms: float) -> WrapperResponse:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ParseError(f"Invalid JSON from model: {exc}") from exc

        required = {"answer", "confidence", "source"}
        missing = required - set(payload.keys())
        if missing:
            raise ParseError(f"Missing keys in model response: {sorted(missing)}")

        answer = str(payload["answer"]).strip()
        confidence = float(payload["confidence"])
        source = str(payload["source"]).strip()

        if not answer:
            raise ParseError("answer cannot be empty")
        if not (0.0 <= confidence <= 1.0):
            raise ParseError("confidence must be in [0, 1]")
        if not source:
            raise ParseError("source cannot be empty")

        return WrapperResponse(
            answer=answer,
            confidence=confidence,
            source=source,
            request_id=request_id,
            latency_ms=latency_ms,
            provider=self.provider,
            model=self.model,
        )


class FakeLLMClient:
    """Local fake client for manual testing."""

    def __init__(self, mode: str = "ok"):
        self.mode = mode
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        if self.mode == "bad_json":
            return "not-json"
        if self.mode == "timeout":
            await asyncio.sleep(5)
            return "{}"
        if self.mode == "transient" and self.calls < 2:
            raise RuntimeError("temporary upstream failure")
        if self.mode == "missing_field":
            return json.dumps({"answer": "Hi", "confidence": 0.8})
        return json.dumps({
            "answer": f"Summary for: {prompt[:30]}",
            "confidence": 0.84,
            "source": "gemini-wrapper-v1",
        })


async def _smoke() -> None:
    wrapper = SimpleLLMWrapper(
        FakeLLMClient(mode="ok"),
        timeout_s=2.0,
        max_retries=2,
        provider="gemini",
        model="gemini-2.0-flash",
    )
    good = await wrapper.ask("What is wrapper vs direct SDK?")
    print("GOOD", good)
    print("GOOD_LOG_FIELDS", good.to_log_fields())

    retry_wrapper = SimpleLLMWrapper(
        FakeLLMClient(mode="transient"),
        timeout_s=2.0,
        max_retries=2,
        provider="gemini",
        model="gemini-2.0-flash",
    )
    recovered = await retry_wrapper.ask("Retry test")
    print("RETRY_RECOVERED", recovered)

    bad = SimpleLLMWrapper(FakeLLMClient(mode="bad_json"), timeout_s=2.0, max_retries=1)
    try:
        await bad.ask("Bad parse test")
    except ParseError as exc:
        print("PARSE_ERROR_OK", str(exc))

    slow = SimpleLLMWrapper(FakeLLMClient(mode="timeout"), timeout_s=0.01, max_retries=1)
    try:
        await slow.ask("Timeout test")
    except GatewayTimeoutError as exc:
        print("TIMEOUT_ERROR_OK", str(exc))


if __name__ == "__main__":
    asyncio.run(_smoke())
