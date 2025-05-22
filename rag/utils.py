import re

def linkify_citations(text: str) -> str:
    base_url = "https://manuelescola.github.io/GenAI_IRPF_chatbot/RENTA_2024.pdf#page="
    return re.sub(
        r"\[p(\d{1,4})\]",
        lambda m: f"[p{m.group(1)}]({base_url}{m.group(1)})",
        text
    )