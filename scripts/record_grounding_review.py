"""Persist the directly read test judgments and construct a complete audit packet.

This is an explicitly disclosed AI-assisted review, not a human label claim.
The decisions are independent of the strict exact-quote hit flags.
"""
import json
from starter_import import ROOT


def read_json(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))


def main():
    traces=[json.loads(line) for line in (ROOT/"results/traces_test.jsonl").read_text(encoding="utf-8").splitlines()]
    pages={p["document_id"]:p for p in map(json.loads,(ROOT/"data/pages.jsonl").read_text(encoding="utf-8").splitlines())}
    grounding,metadata=[],[]
    recorded={(r["strategy"],r["question_id"]):r for r in read_json("results/grounding_labels.json")}
    for t in traces:
        s,qid=t["strategy"],t["question_id"]
        if s=="C":
            b=next(b for b in traces if b["strategy"]=="B" and b["question_id"]==qid)
            assert t["hits"]==b["hits"], "C needs a separate reading if its actual results differ"
        decision=dict(recorded[(s,qid)])
        if decision["reviewed_chunk_ids"]!=[h["chunk_id"] for h in t["hits"]] or decision["score"] not in [0,1,2]:
            raise ValueError("Grounding material changed; do not reuse a saved score")
        grounding.append(decision)
        for h in t["hits"]:
            m=h["metadata"]; p=pages[m["document_id"]]
            assert m["source"]==p["source"] and m["page"]==p["page"] and m["category"]==p["metadata"]["category"]
            assert h["text"]==p["text"][m["char_start"]:m["char_end"]]
            filter_ok=all(m.get(k)==v for k,v in (t["requested_filter"] or {}).items()) if t["requested_filter"] else None
            metadata.append({"strategy":s,"question_id":qid,"rank":h["rank"],"chunk_id":h["chunk_id"],
                "source":m["source"],"page":m["page"],"category":m["category"],"complete_and_correct":True,
                "requested_filter_respected":filter_ok,
                "reason":"URL và page ID khớp module nguồn; category khớp chapter chính thức; char_start/end trỏ đúng text trong snapshot."
                         + (" Metadata đúng nhưng record ngoài phạm vi File Formats yêu cầu (difflib)." if filter_ok is False else ""),
                "reviewer":"Codex — direct inspection of 45 metadata rows plus automatic source-span comparison", "human_confirmed":False})
    labels={"method":"Direct reading by Codex in this session; not an undeclared LLM judge or a claim of student/human review. Coherence read without numeric retrieval scores; grounding read after selection/test. No labels inferred from hit flags.",
            "human_confirmation":"Pending student verification; do not describe these as human-confirmed labels.",
            "coherence":read_json("results/coherence_labels.json"),"grounding":grounding,"metadata":metadata}
    (ROOT/"results/audit_labels.json").write_text(json.dumps(labels,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Hồ sơ đọc và đánh giá mẫu", "", labels["method"], "", "**Chưa có xác nhận của học viên:** " + labels["human_confirmation"], "",
           "## Coherence — cùng 10 vị trí nguồn, 30 nhãn", "", "0: không hiểu do mất ý/chủ thể; 1: hiểu một phần, thiếu ngữ cảnh; 2: tự hiểu và giữ ý. Không lấy Hit@3 làm nhãn.", ""]
    chunks={s:{c["chunk_id"]:c for c in map(json.loads,(ROOT/f"results/chunks_{s}.jsonl").read_text(encoding="utf-8").splitlines())} for s in "ABC"}
    for r in labels["coherence"]:
        c=chunks[r["strategy"]][r["chunk_id"]]
        lines.extend([f"### {r['strategy']} · {r['page']} · {r['score']}/2", "", f"Anchor {r['anchor']}; span [{r['char_start']}, {r['char_end']}); chunk `{r['chunk_id']}`.", "", r["reason"], "", "~~~text", c["text"], "~~~", ""])
    lines.extend(["## Grounding — 5 test × 3 chiến lược", "", "Đọc toàn bộ top-3; đánh giá đủ bằng chứng và điều kiện, có thể dùng nhiều chunk. Không phải độ chính xác câu trả lời LLM. Điểm 2 không có nghĩa literal Evidence Hit@3 phải bằng 1.", ""])
    for t,r in zip(traces,grounding):
        lines.extend([f"### {t['strategy']} · {t['question_id']} · {r['score']}/2", "",t["question"],"", "Đáp án cần hỗ trợ: "+t["expected_answer"],"",r["reason"],""])
        for h in t["hits"]:
            m=h["metadata"]
            lines.extend([f"Rank {h['rank']}: [{m['page']}]({m['source']}), category `{m['category']}`, span [{m['char_start']}, {m['char_end']}); chunk `{h['chunk_id']}`.","", "~~~text",h["text"],"~~~",""])
    lines.extend(["## Metadata — toàn bộ 45 records", "", "Metadata đúng nguồn khác với tuân thủ filter; A/q19/rank3 có metadata đúng nhưng ngoài phạm vi câu hỏi.", "", "| Strategy | Question | Rank | Page | Category | Đủ/đúng | Filter |", "|---|---|---:|---|---|---|---|"])
    for r in metadata:
        flag="N/A" if r["requested_filter_respected"] is None else str(r["requested_filter_respected"])
        lines.append(f"| {r['strategy']} | {r['question_id']} | {r['rank']} | {r['page']} | {r['category']} | Có | {flag} |")
    (ROOT/"results/audit_review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Saved 30 coherence, 15 grounding and 45 metadata AI-assisted review records with full text packets.")

if __name__=="__main__":
    main()
