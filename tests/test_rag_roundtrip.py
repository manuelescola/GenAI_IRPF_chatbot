# tests/test_rag_roundtrip.py
from rag.chat import stream_answer
def test_simple_query():
    out = "".join(stream_answer("¿Qué es el mínimo personal exento?"))
    assert "mínimo personal" in out.lower() or "No tengo" in out