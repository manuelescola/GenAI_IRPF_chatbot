FROM python:3.11-slim

# 1. Basics
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=0

# 2. System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# 3. Project code
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ingest/ ingest/
COPY scripts/ scripts/
COPY rag/ rag/

# 4. Expose volume for persistent Chroma storage
VOLUME ["/app/.chroma"]

# 5. Default command (overridden by docker-compose)
CMD ["python", "-m", "scripts.ingest_pdf", "--help"]
