# rag/chat.py
import os
import re
from typing import Generator
from openai import OpenAI
#from .retriever import ChromaRetriever
from .retriever_pinecone import PineconeRetriever as ChromaRetriever  # temporary alias
from .prompt import make_messages
from .utils import linkify_citations


_MODEL = "gpt-4o" # before I had the following: "gpt-4o-mini"          # or gpt-3.5-turbo
_TEMPERATURE = 0.2

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_answer(question: str) -> Generator[str, None, None]:
    retriever = ChromaRetriever(k=4)
    docs = retriever(question)
    messages = make_messages(question, docs)

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=messages,
        temperature=_TEMPERATURE,
        stream=True,
    )

    full_output = ""

    for chunk in response:
        token = chunk.choices[0].delta.content or ""
        full_output += token

    yield linkify_citations(full_output.strip())
