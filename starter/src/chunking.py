"""Deterministic chunks with exact normalized-source character offsets."""
import hashlib
import re
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    chunks = []
    for start in range(0, len(page.text), size - overlap):
        end = min(start + size, len(page.text))
        chunk = make_chunk(page, start, end)
        if chunk.text:
            chunks.append(chunk)
        if end == len(page.text):
            break
    return chunks


def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    if max_size < 1:
        raise ValueError("max_size must be positive")
    spans = [(m.start(), m.end()) for m in re.finditer(r"\S[\s\S]*?(?=\n\n|\Z)", page.text)]
    chunks, current_start, current_end = [], None, None
    for start, end in spans:
        if current_start is not None and (end - current_start > max_size or page.text[start] == "#"):
            chunks.append(make_chunk(page, current_start, current_end))
            current_start = current_end = None
        while end - start > max_size:
            if current_start is not None:
                chunks.append(make_chunk(page, current_start, current_end))
                current_start = current_end = None
            limit = start + max_size
            candidates = [start + m.end() for m in re.finditer(r"[.!?]\s+|\s+", page.text[start:limit])]
            cut = max((p for p in candidates if p >= start + max_size // 2), default=limit)
            chunks.append(make_chunk(page, start, cut))
            start = cut
        if current_start is None:
            current_start = start
        current_end = end
    if current_start is not None:
        chunks.append(make_chunk(page, current_start, current_end))
    return [chunk for chunk in chunks if chunk.text]


def make_chunk(page, start, end):
    while start < end and page.text[start].isspace():
        start += 1
    while end > start and page.text[end - 1].isspace():
        end -= 1
    text = page.text[start:end]
    digest = hashlib.sha256(f"{page.document_id}|{page.page}|{start}|{end}|{text}".encode()).hexdigest()
    return Chunk(digest, page.document_id, page.source, page.page, text,
                 {**page.metadata, "char_start": start, "char_end": end})
