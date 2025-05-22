from pathlib import Path
from typing import Iterator, List
from pypdf import PdfReader

def _build_outline_map(reader: PdfReader) -> dict[int, List[str]]:
    # Walk bookmarks → map first page index to breadcrumb list
    outline_map = {}
    try:
        for item in reader.outline:
            if hasattr(item, "title"):
                page_idx = reader.get_destination_page_number(item)
                outline_map[page_idx] = item.title.split("—")  # tweak split rule
    except Exception:
        pass
    return outline_map

def iter_pages(pdf_path: Path) -> Iterator[dict]:
    reader = PdfReader(str(pdf_path), strict=False)
    outline = _build_outline_map(reader)
    for i, page in enumerate(reader.pages):
        yield {
            "page": i + 1,
            "toc": outline.get(i, []),
            "text": (page.extract_text() or "").strip()
        }