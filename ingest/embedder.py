# ingest/embedder.py
import os
from openai import OpenAI
from typing import List
import tiktoken

MODEL = "text-embedding-3-large"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Estimate tokens using tiktoken
def count_tokens(text: str, model: str = MODEL) -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def embed(chunks: List[dict]) -> None:
    max_tokens_per_batch = 300000
    batch = []
    token_count = 0

    for chunk in chunks:
        tokens = count_tokens(chunk["text"])
        if token_count + tokens > max_tokens_per_batch:
            # Send current batch
            texts = [c["text"] for c in batch]
            response = client.embeddings.create(model=MODEL, input=texts)
            embeddings = [r.embedding for r in response.data]
            for i, emb in enumerate(embeddings):
                batch[i]["embedding"] = emb
            batch.clear()
            token_count = 0

        batch.append(chunk)
        token_count += tokens

    # Process any remaining batch
    if batch:
        texts = [c["text"] for c in batch]
        response = client.embeddings.create(model=MODEL, input=texts)
        embeddings = [r.embedding for r in response.data]
        for i, emb in enumerate(embeddings):
            batch[i]["embedding"] = emb