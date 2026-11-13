"""Strict evidence hits; gold data is used only after retrieval."""
from collections import defaultdict
from .ingestion import normalize_text
from typing import Any


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    golds = [{"source_id": question["gold_source_id"], "page": question["gold_page"],
              "evidence_quote": question["evidence_quote"]}, *question.get("alternative_gold", [])]
    annotated = []
    for rank, hit in enumerate(hits, 1):
        enough = any(hit["metadata"]["document_id"] == gold["source_id"]
                     and hit["metadata"]["page"] == gold["page"]
                     and normalize_text(gold["evidence_quote"]) in normalize_text(hit["text"])
                     for gold in golds)
        annotated.append({**hit, "rank": rank, "evidence_hit": enough})
    return {"question_id": question["id"], "split": question["split"], "question": question["question"],
            "expected_answer": question["expected_answer"], "golds": golds,
            "requested_filter": question.get("filter"), "hits": annotated,
            "hit1": bool(annotated and annotated[0]["evidence_hit"]),
            "hit3": any(h["evidence_hit"] for h in annotated)}


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = defaultdict(list)
    for trace in traces:
        grouped[(trace["strategy"], trace["split"])].append(trace)
    rows = []
    for (strategy, split), items in sorted(grouped.items()):
        n = len(items)
        h1, h3 = sum(t["hit1"] for t in items), sum(t["hit3"] for t in items)
        filtered = [t for t in items if t["requested_filter"]]
        compliant = sum(len(t["hits"]) == 3 and all(all(h["metadata"].get(k) == v
                         for k, v in t["requested_filter"].items()) for h in t["hits"]) for t in filtered)
        rows.append({"strategy": strategy, "split": split, "n": n, "hit1_n": h1, "hit1": h1 / n,
                     "hit3_n": h3, "hit3": h3 / n, "filter_compliant_n": compliant,
                     "filter_questions_n": len(filtered),
                     "filter_compliance": compliant / len(filtered) if filtered else None})
    return {"rows": rows, "metric": "One top-k chunk must match any gold source/page AND contain the entire evidence quote. Multi-chunk unions do not count."}
