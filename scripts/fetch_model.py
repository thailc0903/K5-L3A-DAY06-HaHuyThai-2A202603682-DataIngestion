"""Fetch the exact audited ONNX model snapshot, then run with HF_HUB_OFFLINE=1."""
import hashlib
import json
from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[1]
REPO = "qdrant/bge-small-en-v1.5-onnx-q"
REVISION = "aa8f8b060edb00e03bfdd08813a2949946c8ba55"
FILES = ["config.json", "model_optimized.onnx", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json"]


def main():
    cache = ROOT / ".cache/models"
    snapshot = Path(snapshot_download(REPO, revision=REVISION, cache_dir=cache, allow_patterns=FILES))
    manifest_path = ROOT / "data/model_manifest.json"
    hashes = {name: hashlib.sha256((snapshot / name).read_bytes()).hexdigest() for name in FILES}
    if manifest_path.exists():
        expected = json.loads(manifest_path.read_text(encoding="utf-8"))
        if expected["files_sha256"] != hashes:
            raise ValueError("Model fingerprint mismatch; do not run with changed weights")
    else:
        manifest_path.write_text(json.dumps({"repo_id": REPO, "revision": REVISION,
            "model_name": "BAAI/bge-small-en-v1.5", "license": "MIT", "dimensions": 384,
            "files_sha256": hashes, "source": f"https://huggingface.co/{REPO}/tree/{REVISION}"}, indent=2) + "\n")
    # FastEmbed resolves 'main' locally. Pin its local ref to this verified snapshot.
    ref = cache / "models--qdrant--bge-small-en-v1.5-onnx-q/refs/main"
    ref.parent.mkdir(parents=True, exist_ok=True)
    ref.write_text(REVISION, encoding="utf-8")
    print(f"Verified {REPO}@{REVISION}; set HF_HUB_OFFLINE=1 before running.")

if __name__ == "__main__":
    main()
