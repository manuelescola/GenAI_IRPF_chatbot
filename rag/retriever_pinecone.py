# rag/retriever_pinecone.py
import os
from pinecone import Pinecone
from openai import OpenAI
from typing import List, Dict

# ✅ New Pinecone client setup
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "irpf-2024"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# ✅ OpenAI embedding client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-large"

class PineconeRetriever:
    def __init__(self, k: int = 4):
        self.k = k

    def __call__(self, query: str) -> List[Dict]:
        # Embed the query
        response = client.embeddings.create(input=[query], model=EMBED_MODEL)
        query_vector = response.data[0].embedding

        # Query Pinecone
        res = index.query(vector=query_vector, top_k=self.k, include_metadata=True)

        return [
            {
                "page": match.metadata.get("page", 0),
                "toc": match.metadata.get("toc", ""),
                "text": match.metadata.get("text", "")
            }
            for match in res.matches
        ]