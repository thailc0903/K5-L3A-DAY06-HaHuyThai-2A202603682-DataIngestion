"""Post-run diagnostics only: measure filter candidate pools without tuning."""
import json
from starter_import import ROOT
from qdrant_client import QdrantClient, models

client=QdrantClient(path=str(ROOT/"results/qdrant"))
try:
    questions=[json.loads(line) for line in (ROOT/"benchmark/questions.jsonl").read_text(encoding="utf-8").splitlines()]
    rows=[]
    for q in questions:
        if not q["filter"]:
            continue
        condition=models.Filter(must=[models.FieldCondition(key=k,match=models.MatchValue(value=v)) for k,v in q["filter"].items()])
        rows.append({"question_id":q["id"],"split":q["split"],"filter":q["filter"],
            "unfiltered_candidate_count":client.count("python313_C",exact=True).count,
            "filtered_candidate_count":client.count("python313_C",count_filter=condition,exact=True).count,
            "purpose":"Post-run candidate-pool diagnostic, not additional tuning or a new retrieval metric"})
    (ROOT/"results/filter_diagnostics.json").write_text(json.dumps(rows,indent=2)+"\n")
    print(json.dumps(rows,indent=2))
finally:
    client.close()
