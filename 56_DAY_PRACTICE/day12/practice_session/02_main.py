from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day12 FastAPI Basics")


class EchoRequest(BaseModel):
    message: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoRequest) -> dict:
    return {"echo": payload.message}
