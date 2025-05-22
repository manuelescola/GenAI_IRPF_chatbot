import re

_PDF_URL = "https://manuelescola.github.io/GenAI_IRPF_chatbot/RENTA_2024.pdf"

def linkify_citations(text: str) -> str:
    return re.sub(
        r"\[p(\d+)\]",
        lambda m: f"[p{m.group(1)}]({_PDF_URL}#page={m.group(1)})",
        text
    )