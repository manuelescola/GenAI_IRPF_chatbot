# ingest/vectordb.py
import os
from pinecone import Pinecone, ServerlessSpec
from typing import List

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = "irpf-2024"

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist (optional safety)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENV
        )
    )

# Connect to index
index = pc.Index(INDEX_NAME)

# Add chunks
def add_chunks(chunks: List[dict]):
    BATCH_SIZE = 100

    vectors = [
        {
            "id": chunk["id"],
            "values": chunk["embedding"],
            "metadata": {
                "text": chunk["text"],
                "page": chunk["metadata"]["page"],
                "toc": chunk["metadata"].get("toc", "")
            },
        }
        for chunk in chunks
    ]

    print(f"🔢 Uploading {len(vectors)} vectors to Pinecone...")

    # Upload in batches
    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i + BATCH_SIZE]
        index.upsert(batch)