"""Measure actual untruncated tokenizer lengths; never estimate from characters."""
import json
from pathlib import Path
from tokenizers import Tokenizer

ROOT = Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"data/model_manifest.json").read_text(encoding="utf-8"))
repo_cache="models--"+manifest["repo_id"].replace("/","--")
path=ROOT/".cache/models"/repo_cache/"snapshots"/manifest["revision"]/"tokenizer.json"
tokenizer = Tokenizer.from_file(str(path))
tokenizer.no_truncation()
tokenizer.no_padding()
rows = []
for strategy in "ABC":
    records = [json.loads(line) for line in (ROOT / f"results/chunks_{strategy}.jsonl").read_text(encoding="utf-8").splitlines()]
    counts = [len(e.ids) for e in tokenizer.encode_batch([r["text"] for r in records])]
    rows.append({"strategy": strategy, "chunks": len(counts), "total_input_tokens_including_special_tokens": sum(counts),
                 "max_tokens": max(counts), "over_512_n": sum(n > 512 for n in counts)})
(ROOT / "results/token_statistics.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
