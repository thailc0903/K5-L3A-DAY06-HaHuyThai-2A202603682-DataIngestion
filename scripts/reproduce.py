"""Replay frozen A/B/C in an isolated store without overwriting baseline artifacts."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from starter_import import ROOT
from starter.src import run

BASELINE_FILES = [
    "benchmark/freeze.json", "benchmark/questions.jsonl", "data/pages.jsonl", "data/manifest.jsonl",
    *[f"results/{name}.json" for name in ["selection","environment_dev","environment_test","ingestion_stats","ingestion_stats_dev","ingestion_stats_test","metrics_dev","metrics_test","persistence_check","coherence_anchors","evidence_validation"]],
    *[f"results/chunks_{s}.jsonl" for s in "ABC"], "results/traces_dev.jsonl", "results/traces_test.jsonl",
]


def fingerprints():
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in BASELINE_FILES}


def load_traces(path):
    return {(t["strategy"],t["question_id"]):t for t in map(json.loads,path.read_text(encoding="utf-8").splitlines())}


def compare_traces(expected,actual):
    if expected.keys()!=actual.keys():
        return False
    for key,before in expected.items():
        after=actual[key]
        for name in ["question","golds","requested_filter","applied_filter","hit1","hit3"]:
            if before[name]!=after[name]:
                return False
        if len(before["hits"])!=len(after["hits"]):
            return False
        for a,b in zip(before["hits"],after["hits"]):
            if any(a[name]!=b[name] for name in ["chunk_id","text","metadata","rank","evidence_hit"]) or abs(a["score"]-b["score"])>1e-6:
                return False
    return True


def main():
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination=ROOT/".cache/reproductions"/stamp
    destination.mkdir(parents=True)
    # Reuse the exact checked model/text cache, but never reuse the vector store.
    cache_source=ROOT/"results/embedding_cache"
    if cache_source.exists():
        shutil.copytree(cache_source,destination/"embedding_cache")
    before=fingerprints()
    report={"started_at_utc":datetime.now(timezone.utc).isoformat(),"output_directory":destination.relative_to(ROOT).as_posix(),
            "store":"New, separate persistent Qdrant store; original store and artifacts untouched",
            "embedding_cache_reused":cache_source.exists(),"fresh_independent_holdout":False,
            "baseline_sha256":before}
    original_out,original_argv=run.OUT,sys.argv
    output=io.StringIO()
    try:
        os.environ["HF_HUB_OFFLINE"]="1"
        run.OUT=destination
        sys.argv=["reproduce","--phase","all"]
        with contextlib.redirect_stdout(output):
            run.main()
        report["checks"]={}
        for split in ["dev","test"]:
            baseline=load_traces(ROOT/f"results/traces_{split}.jsonl")
            replay=load_traces(destination/f"traces_{split}.jsonl")
            report["checks"][f"{split}_all_ranked_texts_metadata_scores_and_hits_match"]=compare_traces(baseline,replay)
            report["checks"][f"{split}_metrics_match"]=json.loads((ROOT/f"results/metrics_{split}.json").read_text())==json.loads((destination/f"metrics_{split}.json").read_text())
        report["checks"]["baseline_artifacts_not_modified"]=before==fingerprints()
        report["checks"]["persisted_reopened"]=json.loads((destination/"persistence_check.json").read_text())["reopened"]
        report["checks"]["selection_matches"]=json.loads((destination/"selection.json").read_text())["selected_strategy"]==json.loads((ROOT/"results/selection.json").read_text())["selected_strategy"]
        report["all_passed"]=all(report["checks"].values())
        report["replay_environment"]=json.loads((destination/"environment_all.json").read_text())
    except Exception as exc:
        report.update(all_passed=False,error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc())
    finally:
        run.OUT,sys.argv=original_out,original_argv
        report["finished_at_utc"]=datetime.now(timezone.utc).isoformat()
        (ROOT/"results/reproduction_run.txt").write_text(output.getvalue(),encoding="utf-8")
        (ROOT/"results/reproduction_check.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in {"baseline_sha256","replay_environment"}},ensure_ascii=False,indent=2))
    if not report["all_passed"]:
        raise SystemExit(1)

if __name__=="__main__":
    main()
