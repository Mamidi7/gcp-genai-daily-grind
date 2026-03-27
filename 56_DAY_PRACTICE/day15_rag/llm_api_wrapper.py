"""Day 15: Minimal LLM API wrapper (local, provider-agnostic)."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Protocol


class ParseError(Exception):
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


class SimpleLLMWrapper:
    def __init__(self, client: LLMClient, timeout_s: float = 8.0, max_retries: int = 2):
        self.client = client
        self.timeout_s = timeout_s
        self.max_retries = max_retries

    async def ask(self, prompt: str) -> WrapperResponse:
        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                raw = await asyncio.wait_for(self.client.generate(prompt), timeout=self.timeout_s)
                return self._parse(raw)
            except ParseError:
                raise
            except Exception as exc:  # timeout / transient upstream errors
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.2 * (attempt + 1))
                    continue
                break

        raise UpstreamError(f"LLM call failed after retries: {last_error}")

    def _parse(self, raw: str) -> WrapperResponse:
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

        return WrapperResponse(answer=answer, confidence=confidence, source=source)


class FakeLLMClient:
    """Local fake client for manual testing."""

    def __init__(self, mode: str = "ok"):
        self.mode = mode
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        if self.mode == "bad_json":
            return "not-json"
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
    wrapper = SimpleLLMWrapper(FakeLLMClient(mode="ok"), timeout_s=2.0, max_retries=2)
    good = await wrapper.ask("What is wrapper vs direct SDK?")
    print("GOOD", good)

    retry_wrapper = SimpleLLMWrapper(FakeLLMClient(mode="transient"), timeout_s=2.0, max_retries=2)
    recovered = await retry_wrapper.ask("Retry test")
    print("RETRY_RECOVERED", recovered)

    bad = SimpleLLMWrapper(FakeLLMClient(mode="bad_json"), timeout_s=2.0, max_retries=1)
    try:
        await bad.ask("Bad parse test")
    except ParseError as exc:
        print("PARSE_ERROR_OK", str(exc))


if __name__ == "__main__":
    asyncio.run(_smoke())
