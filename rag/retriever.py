# rag/retriever.py
from typing import List, Dict
import os, chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

_CHROMA_PATH = ".chroma"
_COLLECTION  = "irpf-2024"

_embed = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-large"
)

class ChromaRetriever:
    def __init__(self, k: int = 4):
        client = chromadb.PersistentClient(path=_CHROMA_PATH)
        self.col = client.get_collection(_COLLECTION)   
        self.k   = k

    def __call__(self, query: str) -> List[Dict]:
        # embed 1 query → returns [vector]; take first element
        query_vec = _embed([query])[0]

        result = self.col.query(
            query_embeddings=[query_vec],
            n_results=self.k,
            include=["documents", "metadatas"]
        )
        docs, metas = result["documents"][0], result["metadatas"][0]
        return [
            {"page": m["page"], "toc": m.get("toc", ""), "text": d}
            for d, m in zip(docs, metas)
        ]
