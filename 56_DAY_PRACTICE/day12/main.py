# day12_fastapi_basics.py | python>=3.12 | requires: fastapi[standard]==0.135.1 pydantic==2.7.1 uvicorn[standard]==0.29.0
"""
Day 12 manual practice app.
Run:
    python3 -m uvicorn main:app --host 127.0.0.1 --port 8012
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Day12 FastAPI Basics", version="1.0.0")


class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}
