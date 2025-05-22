# rag/prompt.py
SYSTEM_PROMPT = """\
Eres un asistente fiscal que responde únicamente en español. 
Cuando cites la normativa, indica la página entre corchetes, p.ej. [p23].
Si la respuesta no está en tu contexto, di "No tengo esa información".\
""".strip()

def make_messages(question: str, context_docs: list[dict]) -> list[dict]:
    # Concatenate contexts with page tags
    context_blocks = [
        f"[p{d['page']}] {d['text']}" for d in context_docs
    ]
    context = "\n\n".join(context_blocks)

    return [
        {"role": "system",    "content": SYSTEM_PROMPT},
        {"role": "user",      "content": f"Pregunta del usuario:\n{question}"},
        {"role": "assistant", "content": "Información relevante encontrada:"},
        {"role": "assistant", "content": context},
        {"role": "user",      "content": "Redacta la respuesta citando las páginas."}
    ]