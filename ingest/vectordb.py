import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path=".chroma",
    settings=Settings(anonymized_telemetry=False)
)
COLLECTION_NAME = "irpf-2024"

def add_chunks(chunks: list[dict]):
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
    )
    print(f"✅  Added {len(chunks)} chunks to {COLLECTION_NAME}")