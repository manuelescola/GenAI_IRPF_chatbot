# scripts/ingest_pdf.py
"""
CLI entrypoint that reads a PDF and stuffs its chunks into Chroma.
Usage:
    python -m scripts.ingest_pdf data/RENTA_2024.pdf
"""
import argparse, pathlib, sys
from ingest import loader, chunker, embedder, vectordb

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path", type=pathlib.Path, help="Path to the source PDF")
    args = ap.parse_args()

    if not args.pdf_path.exists():
        sys.exit(f"❌  File not found: {args.pdf_path}")

    chunks = []
    for page in loader.iter_pages(args.pdf_path):
        chunks.extend(chunker.split_page(page))

    print(f"📝  Parsed {len(chunks)} chunks – now embedding…")
    embedder.embed(chunks)
    vectordb.add_chunks(chunks)
    print("✅  Ingestion complete")

if __name__ == "__main__":
    main()