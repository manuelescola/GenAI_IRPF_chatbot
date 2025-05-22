# GenAI_IRPF_chatbot
This repo creates an AI that helps you prepare the income tax in Spain.

GenAI_IRPF_chatbot/vector_database
│
├─ ingest/                   ← Python package
│   ├─ __init__.py
│   ├─ loader.py             # → extracts pages + TOC
│   ├─ chunker.py            # → two-step splitter
│   ├─ embedder.py           # → OpenAI embeddings
│   └─ vectordb.py           # → Chroma persistence
│
├─ data/                     ← empty; will hold RENTA_2024.pdf
├─ scripts/
│   └─ ingest_pdf.py         # CLI wrapper (entrypoint)
│
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md

GenAI_IRPF_chatbot/chatbot_backend
│
├─ rag/                         ← NEW (pure library code)
│   ├─ __init__.py
│   ├─ retriever.py             # similarity + optional filters
│   ├─ prompt.py                # Spanish templates & citation helpers
│   ├─ chat.py                  # orchestrates RAG turn by turn
│   └─ evaluator.py             # offline quality checks (optional)
│
├─ scripts/
│   └─ serve_rag.py             # FastAPI or simple CLI, your choice
│
├─ configs/
│   └─ rag.yaml                 # tunable params: k, model, temperature…
