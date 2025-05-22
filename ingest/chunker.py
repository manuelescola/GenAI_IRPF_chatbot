from langchain_text_splitters import TokenTextSplitter
_SPLITTER = TokenTextSplitter(chunk_size=500, chunk_overlap=50)

def split_page(page_dict: dict) -> list[dict]:
    toc_list = page_dict.get("toc", [])
    toc_str  = " > ".join(toc_list) if toc_list else ""   # empty string, not None

    chunks = []
    for idx, chunk_text in enumerate(_SPLITTER.split_text(page_dict["text"])):
        metadata = {
            "page": page_dict["page"],        # int → OK
            "source": "RENTA_2024.pdf"        # str → OK
        }
        if toc_str:                           # only add when non-empty
            metadata["toc"] = toc_str

        chunks.append({
            "id": f"p{page_dict['page']}_c{idx}",
            "text": chunk_text,
            "metadata": metadata,
        })
    return chunks
