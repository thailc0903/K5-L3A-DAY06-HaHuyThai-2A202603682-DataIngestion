"""Separate technical integrity from student review and actual submission readiness."""
import hashlib
import json
import subprocess
from pathlib import Path
from starter_import import ROOT
from starter.src.evaluation import evaluate_query, summarize
from starter.src.ingestion import load_jsonl


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    checks = []
    def check(name, condition):
        checks.append({"check": name, "passed": bool(condition)})

    frozen = read_json("benchmark/freeze.json")
    check("Frozen corpus, benchmark, config and retrieval code SHA256", all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == sha for p,sha in frozen["sha256"].items()))
    pages = load_jsonl(ROOT / "data/pages.jsonl")
    indexed = {(p.document_id, p.page): p for p in pages}
    check("At least 30 independent source units >=1500 characters", len(indexed) >= 30 and all(len(p.text)>=1500 for p in pages))
    check("No identical normalized source units", len({p.text for p in pages})==len(pages))
    chunk_coverage=True
    for strategy in "ABC":
        chunks=read_jsonl(f"results/chunks_{strategy}.jsonl")
        for p in pages:
            cursor=0
            for c in sorted((c for c in chunks if c["document_id"]==p.document_id and c["page"]==p.page),key=lambda c:c["metadata"]["char_start"]):
                start,end=c["metadata"]["char_start"],c["metadata"]["char_end"]
                chunk_coverage &= c["text"]==p.text[start:end] and (start<=cursor or not p.text[cursor:start].strip())
                cursor=max(cursor,end)
            chunk_coverage &= not p.text[cursor:].strip()
    check("All chunks preserve exact source offsets and cover every non-whitespace character",chunk_coverage)
    manifest = read_jsonl("data/manifest.jsonl")
    check("Raw/normalized source SHA256, sizes, boundaries and license attribution", all(
        hashlib.sha256((ROOT / m["raw_path"]).read_bytes()).hexdigest()==m["raw_sha256"]
        and hashlib.sha256(indexed[(m["source_id"],m["page_ids"][0])].text.encode()).hexdigest()==m["normalized_sha256"]
        and len(indexed[(m["source_id"],m["page_ids"][0])].text)==m["normalized_characters"]
        and m["boundaries"]=={"start":0,"end":m["normalized_characters"]}
        and m["license_or_permission"] and (ROOT/m["license_snapshot"]).is_file() for m in manifest))
    questions = {q["id"]: q for q in read_jsonl("benchmark/questions.jsonl")}
    check("15 dev / 5 test and >=3 filters including test", sum(q["split"]=="dev" for q in questions.values())>=15 and sum(q["split"]=="test" for q in questions.values())>=5 and sum(bool(q["filter"]) for q in questions.values())>=3 and any(q["filter"] and q["split"]=="test" for q in questions.values()))
    check("Every gold quote appears on exact declared source/page", all(q["evidence_quote"] in indexed[(q["gold_source_id"],q["gold_page"])].text for q in questions.values()))
    splits=read_json("benchmark/splits.json")
    check("Published split lists exactly match benchmark records",all(splits[s]==[q["id"] for q in questions.values() if q["split"]==s] for s in ["dev","test"]))
    traces = read_jsonl("results/traces_dev.jsonl") + read_jsonl("results/traces_test.jsonl")
    check("Complete 60 unique query/strategy traces, three hits each", len(traces)==60 and len({(t['strategy'],t['question_id']) for t in traces})==60 and all(len(t["hits"])==3 for t in traces))
    correct_metrics = True
    for t in traces:
        q = questions[t["question_id"]]
        evaluated = evaluate_query(q,t["hits"])
        correct_metrics &= evaluated["hit1"]==t["hit1"] and evaluated["hit3"]==t["hit3"]
        for h in t["hits"]:
            m=h["metadata"]; p=indexed[(m["document_id"],m["page"])]
            correct_metrics &= p.text[m["char_start"]:m["char_end"]]==h["text"] and m["source"]==p.source and all(m.get(k)==v for k,v in p.metadata.items())
        if t["strategy"]=="C" and q["filter"]:
            correct_metrics &= all(all(h["metadata"][k]==v for k,v in q["filter"].items()) for h in t["hits"])
    check("Hit definitions, all 180 source spans/metadata and C filters", correct_metrics)
    check("Saved split summaries agree with traces", all(summarize([t for t in traces if t["split"]==s])==read_json(f"results/metrics_{s}.json") for s in ["dev","test"]))
    check("B and C chunks exactly identical", (ROOT/"results/chunks_B.jsonl").read_bytes()==(ROOT/"results/chunks_C.jsonl").read_bytes())
    by_pair = {(t["strategy"],t["question_id"]):t for t in traces}
    check("B/C retrieval identical on every unfiltered question", all([(h['chunk_id'],h['score']) for h in by_pair['B',q['id']]['hits']]==[(h['chunk_id'],h['score']) for h in by_pair['C',q['id']]['hits']] for q in questions.values() if not q['filter']))
    selected=read_json("results/selection.json")
    check("Selection retains frozen inputs and records no test metrics used", selected["frozen_hashes"]==frozen["sha256"] and selected["test_metrics_seen"] is False)
    from datetime import datetime
    check("Selection timestamp precedes test-phase run",datetime.fromisoformat(selected["selected_at_utc"])<datetime.fromisoformat(read_json("results/environment_test.json")["run_at_utc"]))
    check("Actual upsert twice preserved all collection counts", all(r["chunk_count"]==r["count_before_reload"]==r["count_after_reload"] for r in read_json("results/ingestion_stats.json")))
    check("Actual persistent store reopened", read_json("results/persistence_check.json")["reopened"])
    labels=read_json("results/audit_labels.json")
    check("30 coherence, 15 grounding, 45 metadata reviewed records", len(labels["coherence"])==30 and len(labels["grounding"])==15 and len(labels["metadata"])==45)
    check("Every subjective label has actual reviewer/reason/valid score", all(r["score"] in [0,1,2] and r["reason"] and r["reviewer"] for r in labels["coherence"]+labels["grounding"]))
    anchors=read_json("results/coherence_anchors.json")
    anchor_keys={(a["document_id"],a["anchor"]) for a in anchors}
    check("Coherence labels use exactly the same ten preregistered source positions",len(anchor_keys)==10 and all({(r["document_id"],r["anchor"]) for r in labels["coherence"] if r["strategy"]==s}==anchor_keys for s in "ABC"))
    check("Grounding judgments identify all three actual test chunks",all(r["reviewed_chunk_ids"]==[h["chunk_id"] for h in by_pair[(r["strategy"],r["question_id"])]["hits"]] for r in labels["grounding"]))
    review=read_json("results/evidence_review_v2.json")
    check("Versioned evidence review binds exact baseline input hashes",all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in review["source_hashes"].items()) and review["post_hoc"] is True and review["independent_holdout"] is False)
    review_rows={(r["strategy"],r["question_id"],r["rank"]):r for r in review["rows"]}
    review_ok=len(review_rows)==180
    for t in traces:
        for h in t["hits"]:
            r=review_rows[(t["strategy"],t["question_id"],h["rank"])]
            review_ok &= r["chunk_id"]==h["chunk_id"] and r["text_sha256"]==hashlib.sha256(h["text"].encode()).hexdigest()
            review_ok &= bool(r["reason"] and r["requirements"] and r["reviewer"])
            review_ok &= r["evidence_hit"]==(h["evidence_hit"] or r["equivalent_accepted"])
            if r["equivalent_accepted"]:
                review_ok &= r["evidence_excerpt"]==h["text"]
    check("All 180 reviewed hits have bound material, criteria and single-chunk decisions",review_ok)
    reviewed_ok=True
    for split in ["dev","test"]:
        rt=read_jsonl(f"results/traces_reviewed_{split}.jsonl")
        expected_summary=summarize(rt)["rows"]
        reviewed_ok &= expected_summary==read_json(f"results/metrics_reviewed_{split}.json")["rows"]
        for t in rt:
            base=by_pair[(t["strategy"],t["question_id"])]
            reviewed_ok &= t["hit1"]==t["hits"][0]["evidence_hit"] and t["hit3"]==any(h["evidence_hit"] for h in t["hits"])
            for a,b in zip(t["hits"],base["hits"]):
                reviewed_ok &= all(a[k]==b[k] for k in ["chunk_id","rank","text","metadata","score"])
                reviewed_ok &= a["evidence_hit"]==review_rows[(t["strategy"],t["question_id"],a["rank"])]["evidence_hit"]
    check("Reviewed metrics use same ranked chunks and one complete chunk per hit",reviewed_ok)
    reproduction=read_json("results/reproduction_check.json")
    check("Real isolated replay matches baseline retrieval and preserves its files",reproduction["all_passed"] and all(reproduction["checks"].values()) and all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in reproduction["baseline_sha256"].items()))
    unit=read_json("results/unit_test_summary.json")
    check("Executed pipeline/review tests succeeded with no skipped tests",unit["successful"] and unit["tests_run"]>=8 and unit["skipped"]==0)
    model=read_json("data/model_manifest.json")
    model_files=reproduction["replay_environment"]["model_files_sha256"]
    check("Replayed embedding model files match the pinned snapshot manifest",all(any(path.endswith('/'+name) and sha==expected for path,sha in model_files.items()) for name,expected in model["files_sha256"].items()))
    protected=["README.md","RUBRIC.md","RULES.md","GUIDE.md","CHECKPOINTS.md","BENCHMARK.md","SUBMISSION.md","REPORT_TEMPLATE.md","report/individual/MSSV_HoTen.md"]
    gitdiff=subprocess.run(["git","diff","--exit-code","HEAD","--",*protected],cwd=ROOT,capture_output=True)
    check("Original rubric, rules, guides, benchmark and report template unchanged",gitdiff.returncode==0)
    check("Required named report and experiment log exist",(ROOT/"report/individual/2A202603682_HaHuyThai.md").exists() and (ROOT/"artifacts/experiment_log.csv").stat().st_size>300)
    from human_review import assess,expected_rows,FORM
    import csv
    with FORM.open(encoding="utf-8-sig",newline="") as stream:
        student_status,_=assess(list(csv.DictReader(stream)),expected_rows())
    technical_ok=all(c["passed"] for c in checks)
    output={"scope":"Technical checks do not certify human grading, commit, repository accessibility or class submission.",
            "technical_checks_passed":technical_ok,"technical_checks_n":len(checks),"checks":checks,
            "student_review":student_status,"rubric_complete":technical_ok and student_status["all_complete"],
            "submission_ready":False,"pending_actions":[
                *([] if student_status["all_complete"] else ["Student must read/confirm or correct subjective and equivalent-evidence labels; no human review is asserted."]),
                "Create the submission commit and record its actual SHA in STUDENT.md.",
                "Verify grader access, push and submit the repository link through the class channel; not performed by this verifier."],
            "limitations":["Reviewed v2 evidence is a disclosed post-hoc AI-assisted evaluation, not a fresh independent holdout.","README and rule documents remain original; run instructions are in docs/RUNNING.md at the student's request."]}
    (ROOT/"results/submission_check.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,ensure_ascii=False,indent=2))
    if not technical_ok:
        raise SystemExit(1)

if __name__=="__main__":
    main()
