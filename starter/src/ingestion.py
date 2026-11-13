"""Unicode normalization and traceable PDF/JSONL readers. No OCR fallback."""
import json
import re
import unicodedata
from pathlib import Path
from .models import DocumentPage


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    from pypdf import PdfReader
    pages = []
    for number, page in enumerate(PdfReader(path).pages, 1):
        text = normalize_text(page.extract_text() or "")
        if not text:
            raise ValueError(f"Empty/scan page requires OCR or explicit exclusion: {path}, page {number}")
        pages.append(DocumentPage(document_id, source, number, text))
    return pages


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ").replace("\x00", "")
    lines = [re.sub(r"[^\S\n]+", " ", line).strip() for line in text.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def load_jsonl(path: Path) -> list[DocumentPage]:
    pages = []
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        record["text"] = normalize_text(record["text"])
        if not record["text"]:
            raise ValueError(f"Empty source unit: {record['document_id']}")
        pages.append(DocumentPage(**record))
    return pages
