"""Prepare and validate an explicit student review form. Never auto-confirm AI labels."""
import csv
import json
from datetime import datetime
try:
    from .starter_import import ROOT
except ImportError:
    from starter_import import ROOT

FORM=ROOT/"results/student_review.csv"
FIELDS=["review_id","kind","strategy","sample","rank","chunk_ids","suggested_score","student_score","student_reason","student_reviewer","student_confirmed","student_reviewed_at"]


def expected_rows():
    labels=json.loads((ROOT/"results/audit_labels.json").read_text(encoding="utf-8"))
    rows=[]
    for kind in ["coherence","grounding","metadata"]:
        for r in labels[kind]:
            sample=r.get("question_id",r.get("document_id"))
            suffix=r.get("rank",r.get("anchor",""))
            rows.append({"review_id":f"{kind}|{r['strategy']}|{sample}|{suffix}","kind":kind,"strategy":r["strategy"],
                "sample":sample,"rank":r.get("rank",""),
                "chunk_ids":";".join(r.get("reviewed_chunk_ids",[r.get("chunk_id","")])),
                "suggested_score":r.get("score",int(r.get("complete_and_correct",False)))})
    evidence=json.loads((ROOT/"results/evidence_review_v2.json").read_text(encoding="utf-8"))
    for r in evidence["rows"]:
        if r["equivalent_accepted"]:
            rows.append({"review_id":f"evidence|{r['strategy']}|{r['question_id']}|{r['rank']}","kind":"evidence", "strategy":r["strategy"],
                "sample":r["question_id"],"rank":r["rank"],"chunk_ids":r["chunk_id"],"suggested_score":1})
    return rows


def assess(rows,expected):
    indexed={r["review_id"]:r for r in rows}
    if len(indexed)!=len(rows) or set(indexed)!={r["review_id"] for r in expected}:
        raise ValueError("Review IDs missing/duplicated or do not match current review material")
    complete,errors=[],[]
    for template in expected:
        row=indexed[template["review_id"]]
        if any(str(row[key])!=str(template[key]) for key in ["kind","strategy","sample","rank","chunk_ids"]):
            raise ValueError("Review identifiers/material changed")
        if not any(row.get(key,"").strip() for key in ["student_score","student_reason","student_reviewer","student_confirmed","student_reviewed_at"]):
            continue
        valid=True
        if row.get("student_confirmed","").strip().lower()!="yes":
            valid=False
        try:
            score=int(row.get("student_score",""))
            valid &= score in ({0,1,2} if row["kind"] in {"coherence","grounding"} else {0,1})
            at=datetime.fromisoformat(row.get("student_reviewed_at",""))
            valid &= at.tzinfo is not None
        except ValueError:
            valid=False
        valid &= bool(row.get("student_reason","").strip()) and bool(row.get("student_reviewer","").strip())
        if valid:
            complete.append(row)
        else:
            errors.append(row["review_id"])
    return {"form":FORM.relative_to(ROOT).as_posix(),"expected_records":len(expected),"completed_records":len(complete),
        "core_expected_records":90,"core_completed_records":sum(r["kind"]!="evidence" for r in complete),
        "all_complete":len(complete)==len(expected) and not errors,"invalid_rows":errors,
        "status":"complete" if len(complete)==len(expected) and not errors else "pending_student_review",
        "note":"Blank fields remain pending. suggested_score is AI output, never student confirmation."},complete


def main():
    expected=expected_rows()
    if not FORM.exists():
        with FORM.open("w",encoding="utf-8-sig",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=FIELDS);writer.writeheader()
            for row in expected:
                writer.writerow(row)
    with FORM.open(encoding="utf-8-sig",newline="") as stream:
        rows=list(csv.DictReader(stream))
    status,complete=assess(rows,expected)
    (ROOT/"results/human_review_status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if status["all_complete"]:
        (ROOT/"results/human_review.json").write_text(json.dumps({"method":"Student-entered row-level review; no AI auto-confirmation", "rows":complete},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(status,ensure_ascii=False,indent=2))
    if status["invalid_rows"]:
        raise SystemExit(1)

if __name__=="__main__":
    main()
