"""Fill the supplied report outline without changing its headings/prompts/tables."""
import csv
import json
import re
from collections import Counter
from starter_import import ROOT


def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))


def verify_outline(template,report):
    for pattern,name in [(r"^#{1,6} .+$","headings"),(r"^\|[^\n]+\|$","tables")]:
        expected=re.findall(pattern,template,re.M)
        actual=re.findall(pattern,report,re.M)
        if name=="headings":
            if actual!=expected:
                raise ValueError("Report headings must exactly match the supplied template")
        else:
            # The template owns both table headers and separator rows; only data rows are added.
            if [line for line in actual if line in expected]!=expected:
                raise ValueError("Report table headers/separators must remain unchanged")
            if len([line for line in actual if line.startswith("| Strategy |")])!=2:
                raise ValueError("The report must retain exactly the two supplied tables")
    expected=[line for line in template.splitlines() if line.startswith("- ")]
    actual=[line for line in report.splitlines() if line.startswith("- ")]
    if len(actual)!=len(expected) or any(not line.startswith(prompt+" ") for prompt,line in zip(expected,actual)):
        raise ValueError("Report bullet prompts/order must exactly follow the supplied outline")


def main():
    template=(ROOT/"REPORT_TEMPLATE.md").read_text(encoding="utf-8")
    individual_template=(ROOT/"report/individual/MSSV_HoTen.md").read_text(encoding="utf-8")
    if template!=individual_template:
        raise ValueError("Report templates disagree; do not silently change the supplied outline")
    metrics=read("results/metrics_dev.json")["rows"]+read("results/metrics_test.json")["rows"]
    reviewed=read("results/metrics_reviewed_dev.json")["rows"]+read("results/metrics_reviewed_test.json")["rows"]
    stats={r["strategy"]:r for r in read("results/ingestion_stats.json")}
    tokens={r["strategy"]:r for r in read("results/token_statistics.json")}
    labels=read("results/audit_labels.json")
    selected=read("results/selection.json")
    environment=read("results/environment_dev.json")
    model=read("data/model_manifest.json")
    manifest=[json.loads(line) for line in (ROOT/"data/manifest.jsonl").read_text(encoding="utf-8").splitlines()]
    corpus_chars=sum(r["normalized_characters"] for r in manifest)
    versions=", ".join(sorted({r["version"] for r in manifest}))
    chunks_reduced=1-stats["B"]["chunk_count"]/stats["A"]["chunk_count"]
    token_reduced=1-tokens["B"]["total_input_tokens_including_special_tokens"]/tokens["A"]["total_input_tokens_including_special_tokens"]
    context={
        "version":versions,"units":len(manifest),"characters":f"{corpus_chars:,}",
        "fastembed":environment["packages"]["fastembed"],"dimensions":model["dimensions"],
        "qdrant":environment["packages"]["qdrant-client"],"selected":selected["selected_strategy"],
        "chunk_reduction":f"{chunks_reduced:.2%}","token_reduction":f"{token_reduced:.2%}",
        "a_embedding":f"{stats['A']['embedding_seconds']:.2f}","b_embedding":f"{stats['B']['embedding_seconds']:.2f}",
    }
    answers=[answer.format(**context) for answer in read("scripts/report_answers.json")]
    prompts=[line for line in template.splitlines() if line.startswith("- ")]
    if len(prompts)!=len(answers):
        raise ValueError("Unexpected supplied outline; review it before generating the report")
    report=template
    for prompt,answer in zip(prompts,answers):
        report=report.replace(prompt,prompt+" "+answer,1)
    rows=[]
    for s in "ABC":
        for split in ["dev","test"]:
            m=next(r for r in metrics if r["strategy"]==s and r["split"]==split)
            v=next(r for r in reviewed if r["strategy"]==s and r["split"]==split)
            rows.append(f"| {s} | {split} | {m['hit1_n']}/{m['n']}; v2 {v['hit1_n']}/{v['n']} | {m['hit3_n']}/{m['n']}; v2 {v['hit3_n']}/{v['n']} | {stats[s]['chunk_count']} | {stats[s]['ingest_seconds']:.2f} s"+(" (cache B)" if s=="C" else "")+" | 0 USD |")
    first="|---|---|---|---|---|---|---|"
    legend="Trước dấu chấm phẩy: literal gốc; v2: [evidence tương đương do AI rà soát sau test](../../results/evidence_review_v2.md), chưa có học viên xác nhận, không đổi cấu hình/ranking. Hit cần một chunk đủ evidence. Thời gian ingest không gồm reload; C tái dùng embedding B."
    report=report.replace(first,first+"\n"+"\n".join(rows)+"\n\n"+legend,1)
    rows=[]
    for s in "ABC":
        coherence=[r["score"] for r in labels["coherence"] if r["strategy"]==s]
        grounding=[r["score"] for r in labels["grounding"] if r["strategy"]==s]
        meta=[r for r in labels["metadata"] if r["strategy"]==s]
        m=next(r for r in metrics if r["strategy"]==s and r["split"]=="test")
        hist=Counter(grounding)
        rows.append(f"| {s} | {sum(coherence)/len(coherence):.2f}/2 (10) | {sum(r['complete_and_correct'] for r in meta)}/{len(meta)} | {m['filter_compliant_n']}/{m['filter_questions_n']} | {hist[0]}/{hist[1]}/{hist[2]}; trung bình {sum(grounding)/len(grounding):.2f}/2 |")
    second="|---|---|---|---|---|"
    report=report.replace("\n"+second+"\n","\n"+second+"\n"+"\n".join(rows)+"\n",1)
    trace_prompt="Đường dẫn trace, nhãn thủ công và cách chọn mẫu:"
    trace_answer=" [Dev](../../results/traces_dev.jsonl), [test](../../results/traces_test.jsonl), [nhãn và lý do](../../results/audit_labels.json). Coherence: cùng 10 vị trí nguồn theo thứ tự source_id, giữa đoạn đầu ≥150 ký tự, chốt trước retrieval. Metadata: 45 records test. Grounding: 5 test/chiến lược. Thang điểm theo GUIDE; Codex đánh giá AI hỗ trợ, chưa có học viên xác nhận thủ công."
    report=report.replace(trace_prompt,trace_prompt+trace_answer,1)
    # CommonMark requires a blank line before the existing lists and tables.
    report=re.sub(r"(## [^\n]+)\n(?=[-|])",r"\1\n\n",report)
    verify_outline(template,report)
    target=ROOT/"report/individual/2A202603682_HaHuyThai.md"
    target.write_text(report,encoding="utf-8")
    fields=["strategy","chunking","chunk_size","overlap","metadata","filter","vectorizer","hypothesis","dev_hit1","dev_hit3","test_hit1","test_hit3","notes"]
    hypotheses={"A":"Baseline fixed windows may cut evidence/conditions.","B":"Paragraph grouping should improve context but can dilute short API facts.","C":"With trusted question context, category filter narrows scope; accuracy uplift is not guaranteed."}
    with (ROOT/"artifacts/experiment_log.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for s in "ABC":
            d=next(m for m in metrics if m["strategy"]==s and m["split"]=="dev")
            t=next(m for m in metrics if m["strategy"]==s and m["split"]=="test")
            writer.writerow({"strategy":s,"chunking":"fixed" if s=="A" else "heading_paragraph","chunk_size":500 if s=="A" else 1000,"overlap":50 if s=="A" else 0,
                "metadata":"document_id;source;page;category;version;language;module;document_type;char_start;char_end",
                "filter":"category only when supplied in question" if s=="C" else "none",
                "vectorizer":f"BAAI/bge-small-en-v1.5;384;ONNX;revision {model['revision']}","hypothesis":hypotheses[s],
                "dev_hit1":f"{d['hit1_n']}/{d['n']}","dev_hit3":f"{d['hit3_n']}/{d['n']}","test_hit1":f"{t['hit1_n']}/{t['n']}","test_hit3":f"{t['hit3_n']}/{t['n']}",
                "notes":"Measured 2026-11-13; exact quote metric; no test tuning; AI-assisted labels disclosed; C reuses B embeddings; selection C by predeclared tie-break."})
    print("Filled the original four-section outline: same title, 11 prompts and two table schemas.")

if __name__=="__main__":
    main()
