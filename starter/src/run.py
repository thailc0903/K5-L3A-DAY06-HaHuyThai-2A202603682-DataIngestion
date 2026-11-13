"""Run from repo root: python -m starter.src.run --phase dev|test|all."""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import re
import time
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from .chunking import fixed_size, by_paragraph
from .embeddings import MyEmbedder
from .evaluation import evaluate_query, summarize
from .ingestion import load_jsonl, normalize_text
from .store import QdrantStore

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze(pages, questions, config):
    indexed = {(p.document_id, p.page): p for p in pages}
    if len(indexed) < 30 or any(len(p.text) < 1500 for p in pages):
        raise ValueError("Need >=30 unique, nonempty content units >=1500 characters")
    if len({hashlib.sha256(p.text.encode()).hexdigest() for p in pages}) != len(pages):
        raise ValueError("Duplicate source units")
    if len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Duplicate question IDs")
    for split, minimum in [("dev", 15), ("test", 5)]:
        if sum(q["split"] == split for q in questions) < minimum:
            raise ValueError("Insufficient benchmark split")
    filtered = [q for q in questions if q.get("filter")]
    if len(filtered) < 3 or not any(q["split"] == "test" for q in filtered):
        raise ValueError("Insufficient metadata questions")
    validations = []
    for q in questions:
        golds = [{"source_id": q["gold_source_id"], "page": q["gold_page"], "evidence_quote": q["evidence_quote"]}, *q.get("alternative_gold", [])]
        for gold in golds:
            page = indexed[(gold["source_id"], gold["page"])]
            quote = normalize_text(gold["evidence_quote"])
            start = page.text.find(quote)
            if start < 0:
                raise ValueError(f"Evidence absent: {q['id']}")
            for key, value in q.get("filter", {}).items():
                if key not in QdrantStore.ALLOWED_FILTERS or page.metadata.get(key) != value:
                    raise ValueError(f"Invalid filter: {q['id']}")
            validations.append({"question_id": q["id"], "source_id": page.document_id,
                                "page": page.page, "evidence_start": start, "evidence_end": start + len(quote), "verified": True})
    hashes = {p: digest(ROOT / p) for p in ["data/pages.jsonl", "data/manifest.jsonl", "benchmark/questions.jsonl", "configs/strategies.json"]}
    # Also freeze retrieval implementation: changes after selection cannot silently reuse holdout.
    hashes.update({p.relative_to(ROOT).as_posix(): digest(p) for p in sorted((ROOT / "starter/src").glob("*.py"))})
    lock_path = ROOT / "benchmark/freeze.json"
    if lock_path.exists():
        if json.loads(lock_path.read_text(encoding="utf-8"))["sha256"] != hashes:
            raise ValueError("Frozen experiment inputs changed. Archive old run and explicitly declare a new non-independent experiment.")
    else:
        write_json(lock_path, {"frozen_at_utc": datetime.now(timezone.utc).isoformat(), "sha256": hashes,
                   "selection_rule": config["selection_rule"], "split_policy": "15 dev / 5 test; test topics reserved before retrieval; authors know golds by construction, no test score used in selection."})
    write_json(OUT / "evidence_validation.json", validations)
    anchors = []
    for page in sorted(pages, key=lambda p: p.document_id)[:10]:
        paragraphs = list(re.finditer(r"\S[\s\S]*?(?=\n\n|\Z)", page.text))
        prose = next(m for m in paragraphs if len(m.group()) >= 150 and not m.group().startswith("#"))
        anchors.append({"document_id": page.document_id, "page": page.page,
                        "anchor": (prose.start() + prose.end()) // 2,
                        "source_paragraph": prose.group(), "paragraph_start": prose.start(), "paragraph_end": prose.end()})
    write_json(OUT / "coherence_anchors.json", anchors)
    return hashes, anchors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["dev", "test", "all"], default="all")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    config = json.loads((ROOT / "configs/strategies.json").read_text(encoding="utf-8"))
    pages = load_jsonl(ROOT / "data/pages.jsonl")
    questions = read_jsonl(ROOT / "benchmark/questions.jsonl")
    hashes, anchors = freeze(pages, questions, config)
    started = time.perf_counter()
    embedder = MyEmbedder(config["model_name"], str(ROOT / ".cache/models"))
    if embedder.dimensions != config["dimensions"]:
        raise ValueError("Model/config dimension mismatch")
    model_seconds = time.perf_counter() - started
    model_files = {p.relative_to(ROOT / ".cache/models").as_posix(): digest(p)
                   for p in (ROOT / ".cache/models").rglob("*") if p.is_file() and p.suffix in {".onnx", ".json", ".txt"}}
    write_json(OUT / f"environment_{args.phase}.json", {"python": platform.python_version(), "platform": platform.platform(),
        "packages": {name: importlib.metadata.version(name) for name in ["fastembed", "qdrant-client", "onnxruntime", "numpy", "tokenizers", "beautifulsoup4", "requests"]},
        "model_name": embedder.model_name, "dimensions": embedder.dimensions, "model_files_sha256": model_files,
        "document_preprocessing": "FastEmbed passage_embed", "query_preprocessing": "FastEmbed query_embed",
        "metric": "cosine", "search": "Qdrant local exact dense search", "model_init_seconds": model_seconds,
        "api_cost_usd": 0, "cost_scope": "No paid API; excludes electricity, hardware, network and human time",
        "run_at_utc": datetime.now(timezone.utc).isoformat()})
    cache = OUT / "embedding_cache"
    cache.mkdir(exist_ok=True)
    store = QdrantStore(str(OUT / "qdrant"), embedder.dimensions)
    store.create_schema()
    stats, samples = [], []
    all_chunks = {}
    model_identity = hashlib.sha256(json.dumps(model_files, sort_keys=True).encode()).hexdigest()
    try:
        for strategy, params in config["strategies"].items():
            t0 = time.perf_counter()
            chunks = [chunk for page in pages for chunk in (
                fixed_size(page, params["chunk_size"], params["overlap"]) if params["chunking"] == "fixed"
                else by_paragraph(page, params["chunk_size"]))]
            all_chunks[strategy] = chunks
            text_key = hashlib.sha256((model_identity + "\0" + "\0".join(c.text for c in chunks)).encode()).hexdigest()
            cache_path = cache / f"{text_key}.npz"
            cached = cache_path.exists()
            t_embed = time.perf_counter()
            if cached:
                vectors = np.load(cache_path)["vectors"]
            else:
                print(f"Embedding {strategy}: {len(chunks)} chunks", flush=True)
                vectors = np.asarray(embedder.embed_documents([c.text for c in chunks]), dtype=np.float32)
                np.savez_compressed(cache_path, vectors=vectors)
            embedding_seconds = time.perf_counter() - t_embed
            t_store = time.perf_counter()
            store.upsert(strategy, chunks, vectors.tolist())
            first_count = store.count(strategy)
            store_seconds = time.perf_counter() - t_store
            t_reload = time.perf_counter()
            store.upsert(strategy, chunks, vectors.tolist())
            reloaded_count = store.count(strategy)
            if first_count != len(chunks) or reloaded_count != first_count:
                raise ValueError("Idempotency check failed")
            lengths = [len(c.text) for c in chunks]
            stats.append({"strategy": strategy, "chunk_count": len(chunks), "total_characters": sum(lengths),
                "length_min": min(lengths), "length_p50": float(np.median(lengths)), "length_p95": float(np.percentile(lengths, 95)),
                "length_max": max(lengths), "embedding_seconds": embedding_seconds, "embedding_cached": cached,
                "store_seconds": store_seconds, "ingest_seconds": t_store + store_seconds - t0,
                "ingest_and_reload_seconds": time.perf_counter() - t0,
                "reload_seconds": time.perf_counter() - t_reload, "count_before_reload": first_count,
                "count_after_reload": reloaded_count, "api_cost_usd": 0})
            (OUT / f"chunks_{strategy}.jsonl").write_text("".join(json.dumps(asdict(c), ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
            for anchor in anchors:
                chunk = min((c for c in chunks if c.document_id == anchor["document_id"] and
                            c.metadata["char_start"] <= anchor["anchor"] < c.metadata["char_end"]),
                            key=lambda c: c.metadata["char_start"])
                samples.append({"strategy": strategy, **anchor, "chunk": asdict(chunk),
                                "score": None, "reason": "", "reviewer": ""})
        write_json(OUT / f"ingestion_stats_{args.phase}.json", stats)
        if not (OUT / "ingestion_stats.json").exists():
            write_json(OUT / "ingestion_stats.json", stats)
        write_json(OUT / "coherence_review_packet.json", samples)
        # Close/reopen the actual on-disk client before benchmarking to verify persistence.
        store.close()
        store = QdrantStore(str(OUT / "qdrant"), embedder.dimensions)
        persistence = {s: store.count(s) for s in ("A", "B", "C")}
        assert persistence == {r["strategy"]: r["chunk_count"] for r in stats}
        write_json(OUT / "persistence_check.json", {"reopened": True, "counts": persistence})
        query_vectors = {q["id"]: embedder.embed_query(q["question"]) for q in questions if args.phase == "all" or q["split"] == args.phase}
        phases = ["dev", "test"] if args.phase == "all" else [args.phase]
        for split in phases:
            if split == "test":
                selection = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
                if selection["frozen_hashes"] != hashes:
                    raise ValueError("Selection does not match frozen inputs")
            traces = []
            for strategy, params in config["strategies"].items():
                for q in (q for q in questions if q["split"] == split):
                    filters = q.get("filter") if params["use_filter"] else None
                    t0 = time.perf_counter()
                    # Only the question and its predeclared user-context filter enter retrieval.
                    hits = store.search(strategy, query_vectors[q["id"]], config["top_k"], filters)
                    elapsed = time.perf_counter() - t0
                    trace = evaluate_query(q, hits)
                    trace.update(strategy=strategy, applied_filter=filters, retrieval_seconds=elapsed)
                    traces.append(trace)
            (OUT / f"traces_{split}.jsonl").write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in traces), encoding="utf-8")
            summary = summarize(traces)
            write_json(OUT / f"metrics_{split}.json", summary)
            print(json.dumps(summary, indent=2), flush=True)
            if split == "dev":
                sizes = {r["strategy"]: r["total_characters"] for r in stats}
                preference = {"C": 2, "B": 1, "A": 0}
                selected = max(summary["rows"], key=lambda r: (r["hit3"], r["hit1"], -sizes[r["strategy"]], preference[r["strategy"]]))
                selection = {"selected_strategy": selected["strategy"], "selected_at_utc": datetime.now(timezone.utc).isoformat(),
                             "rule": config["selection_rule"], "dev_results": summary["rows"], "frozen_hashes": hashes,
                             "test_metrics_seen": False}
                if (OUT / "selection.json").exists() and json.loads((OUT / "selection.json").read_text())["selected_strategy"] != selected["strategy"]:
                    raise ValueError("Dev selection changed; preserve prior test history")
                write_json(OUT / "selection.json", selection)
    finally:
        store.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        with (OUT / "errors.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"at_utc": datetime.now(timezone.utc).isoformat(),
                "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}, ensure_ascii=False) + "\n")
        raise
