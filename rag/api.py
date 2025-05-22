# rag/api.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .chat import stream_answer

app = FastAPI()

@app.get("/chat")
def chat(q: str):
    gen = (token for token in stream_answer(q))
    return StreamingResponse(gen, media_type="text/event-stream")
