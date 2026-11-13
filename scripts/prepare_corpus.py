"""Download an attributable, checksummed Python 3.13 documentation snapshot."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))
from src.ingestion import normalize_text

CHAPTERS = {
    "text": ["string", "re", "difflib", "textwrap", "unicodedata"],
    "binary": ["struct", "codecs"],
    "datatypes": ["collections", "collections.abc", "heapq", "bisect", "array", "copy", "pprint", "datetime"],
    "numeric": ["decimal", "fractions", "statistics"],
    "filesys": ["pathlib", "os.path", "filecmp", "tempfile", "glob", "fnmatch", "shutil"],
    "persistence": ["pickle", "sqlite3"],
    "fileformats": ["csv", "configparser"],
    "netdata": ["json"],
    "archiving": ["gzip", "zipfile"],
}
BASE = "https://docs.python.org/3.13/"


def main():
    raw_dir = ROOT / "data/raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "Day06-TechnicalDocs-StudentLab/1.0"
    events = []
    manifest_path = ROOT / "data/manifest.jsonl"
    previous = {m["source_id"]: m for m in map(json.loads, manifest_path.read_text(encoding="utf-8").splitlines())} if manifest_path.exists() else {}

    def get(relative):
        target = raw_dir / relative.replace("/", "__")
        if not target.exists():
            response = session.get(BASE + relative, timeout=90)
            response.raise_for_status()
            target.write_bytes(response.content)
        return target, BeautifulSoup(target.read_bytes(), "html.parser")

    try:
        _, license_soup = get("license.html")
        get("copyright.html")
        get("library/index.html")
        (ROOT / "data/LICENSE-PYTHON.txt").write_text(
            license_soup.select_one('div[role="main"]').get_text("\n", strip=True), encoding="utf-8")
        pages, manifest = [], []
        for chapter, modules in CHAPTERS.items():
            _, chapter_soup = get(f"library/{chapter}.html")
            category = chapter_soup.select_one("h1").get_text(" ", strip=True).replace("¶", "").strip()
            chapter_links = {a.get("href", "").split("#")[0] for a in chapter_soup.select("a[href]")}
            for module in modules:
                assert f"{module}.html" in chapter_links, (module, chapter)
                raw_path, soup = get(f"library/{module}.html")
                main = soup.select_one('div[role="main"]')
                assert main is not None, module
                for useless in main.select(".headerlink, .viewcode-link, .toc-backref"):
                    useless.decompose()
                blocks = []
                for node in main.find_all(["h1", "h2", "h3", "h4", "p", "pre", "dt", "td", "th"]):
                    if node.find_parent(["pre", "p", "dt", "td", "th"]):
                        continue
                    block = node.get_text(" ", strip=True)
                    if node.name.startswith("h"):
                        block = "#" * int(node.name[1]) + " " + block
                    if block.strip():
                        blocks.append(block)
                text = normalize_text("\n\n".join(blocks))
                assert len(text) >= 1500, (module, len(text))
                source_id = "py313-" + module
                raw_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
                previous_entry = previous.get(source_id, {})
                accessed_at = previous_entry.get("accessed_at") if previous_entry.get("raw_sha256") == raw_sha else datetime.now(timezone.utc).isoformat()
                version_match = re.search(r"Python (3\.13\.[\d]+) documentation", soup.title.get_text())
                version = version_match.group(1) if version_match else "3.13 (snapshot)"
                source = BASE + f"library/{module}.html"
                pages.append({"document_id": source_id, "source": source, "page": module,
                    "text": text, "metadata": {"category": category, "version": version,
                    "language": "en", "module": module, "document_type": "technical_reference"}})
                manifest.append({"source_id": source_id, "title": main.select_one("h1").get_text(" ", strip=True),
                    "source_path_or_url": source, "raw_path": raw_path.relative_to(ROOT).as_posix(),
                    "license_or_permission": "PSF-2.0; code examples additionally 0BSD",
                    "license_url": BASE + "license.html", "license_snapshot": "data/LICENSE-PYTHON.txt",
                    "accessed_at": accessed_at, "version": version,
                    "page_ids": [module], "physical_pages": None, "counted_content_units": 1,
                    "counting_rule": "One independent official module reference, >=1500 normalized characters; main content only; no duplicate padding.",
                    "boundaries": {"start": 0, "end": len(text)}, "normalized_characters": len(text),
                    "raw_sha256": raw_sha,
                    "normalized_sha256": hashlib.sha256(text.encode()).hexdigest(),
                    "category": category, "category_source": BASE + f"library/{chapter}.html",
                    "modifications": "Extract main prose/API/code/table blocks; drop navigation and pilcrow anchors; normalize Unicode NFC and whitespace."})
                events.append({"source_id": source_id, "status": "ok", "characters": len(text), "ocr": "not_needed"})
                print(f"{module}: {len(text)} characters", flush=True)
        assert len(pages) >= 30
        assert len({hashlib.sha256(p['text'].encode()).hexdigest() for p in pages}) == len(pages)
        for filename, records in [("pages.jsonl", pages), ("manifest.jsonl", manifest)]:
            (ROOT / "data" / filename).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    except Exception as exc:
        events.append({"status": "error", "error_type": type(exc).__name__, "message": str(exc)})
        raise
    finally:
        (ROOT / "results").mkdir(exist_ok=True)
        with (ROOT / "results/corpus_processing.jsonl").open("a", encoding="utf-8") as stream:
            for event in events:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
