import os, time
import openai
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)

@retry(wait=wait_exponential(multiplier=1, min=1, max=60),
       stop=stop_after_attempt(6))
def _emb(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        input=texts,
        model="text-embedding-3-large"
    )
    return [d.embedding for d in resp.data]

def embed(chunks: list[dict], batch_size: int = 96):
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectors = _emb([c["text"] for c in batch])
        for c, v in zip(batch, vectors):
            c["embedding"] = v