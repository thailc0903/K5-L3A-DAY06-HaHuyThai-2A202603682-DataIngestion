# Data Ingestion — Tài liệu kỹ thuật Python 3.13

**Hà Huy Thái · 2A202603682 · lớp 3A**

Bài thực nghiệm so sánh fixed-size chunking, chunking theo cấu trúc và metadata filter trên **32 tài liệu module độc lập** của thư viện chuẩn Python. Corpus tiếng Anh; benchmark 15 dev / 5 test; báo cáo tiếng Việt. Embedding thật chạy local bằng FastEmbed/BGE, lưu bền vững bằng Qdrant, không cần API key hay Docker.

Đọc [báo cáo cá nhân](../report/individual/2A202603682_HaHuyThai.md), [giao thức chốt benchmark](../benchmark/PROTOCOL.md), [ghi chú giải thích bài](../docs/DEFENSE_NOTES.md) và [nhật ký thiết lập](../results/setup_notes.md). Các tệp đề bài RUBRIC, RULES, GUIDE, CHECKPOINTS và BENCHMARK được giữ nguyên.

## Cài đặt và chạy lại

Đã kiểm tra trên Windows, CPython 3.12.16, CPU. Cần mạng lần đầu để tải thư viện và khoảng 67 MB model; corpus HTML đã có trong repo. Chạy từ **root repo**, không phải `starter/`. Ví dụ PowerShell với `uv`:

```powershell
if (-not (Test-Path .venv/Scripts/python.exe)) { uv venv --python 3.12 .venv }
uv pip install --python .venv/Scripts/python.exe -r requirements.lock
$env:HF_HUB_OFFLINE = '0'
.venv/Scripts/python.exe scripts/fetch_model.py
$env:HF_HUB_OFFLINE = '1'
$env:PYTHONIOENCODING = 'utf-8'
.venv/Scripts/python.exe scripts/check_tests.py
.venv/Scripts/python.exe scripts/reproduce.py
.venv/Scripts/python.exe scripts/review_evidence.py
.venv/Scripts/python.exe scripts/token_statistics.py
.venv/Scripts/python.exe scripts/human_review.py
.venv/Scripts/python.exe scripts/verify_submission.py
.venv/Scripts/python.exe scripts/build_report.py
```

Có thể thay `uv pip install` bằng `python -m pip install` trong venv. Trên macOS/Linux dùng `.venv/bin/python` và `export HF_HUB_OFFLINE=1`; phiên bản lock có marker cho gói riêng của Windows, nhưng nền tảng khác chưa được chạy trong phiên này. Không chạy hai tiến trình mở cùng đường dẫn Qdrant local. Không tạo lại `.venv` đang có nếu chỉ muốn chạy lại; việc tạo mới có thể xóa dependencies đã cài.

`reproduce.py` dùng mã pipeline đã khóa nhưng tạo **store riêng mới** trong `.cache/reproductions/<timestamp>/`, chạy dev → lưu selection → test, so sánh toàn bộ ranking/text/metadata/score/hit với kết quả gốc và xác nhận checksum artifact gốc không đổi. Có thể dùng lại embedding cache đúng fingerprint để tiết kiệm thời gian; đây vẫn là model thật, không phải mock. Lượt chạy thực đã kiểm chứng ở `results/reproduction_check.json` và `reproduction_run.txt`.

CLI gốc vẫn là `.venv/Scripts/python.exe -m starter.src.run --phase dev` rồi `--phase test`; nó ghi vào `results/` và có thể thay timestamp/trace/environment của lượt trước. Với bài đã có kết quả, nên dùng replay cô lập ở trên để giữ bằng chứng. Chạy lại cùng dữ liệu/cấu hình không tạo một holdout độc lập mới.

`fetch_model.py` lấy đúng revision trong `data/model_manifest.json`, kiểm tra SHA-256 rồi khóa ref local. Khi chạy offline, không âm thầm tải phiên bản model khác. Cache embedding có khóa theo fingerprint model và toàn bộ chunk text; lỗi model/store dừng chương trình và ghi `results/errors.jsonl`.

Mỗi phase đồng bộ lại ba collection và upsert lần hai để kiểm tra idempotency; đóng/mở store trước retrieval để kiểm tra persistence. Số liệu lần ingest đầu được giữ trong `ingestion_stats.json`; thống kê chạy lại nằm ở các tệp `_dev`/`_test`, không coi thời gian cache là thời gian embedding mới.

## Corpus, benchmark và cấu hình

- `data/raw/`: HTML gốc và chapter xác nhận category; `data/LICENSE-PYTHON.txt`: nội dung giấy phép; `data/manifest.jsonl`: URL, quyền sử dụng, snapshot version, thời điểm truy cập, ranh giới và checksum.
- `data/pages.jsonl`: 32 đơn vị nội dung sau chuẩn hóa NFC; mỗi module là một page ID có ý nghĩa, tất cả ≥1.500 ký tự. Không lấy số chunk làm số trang và không nhân bản nội dung.
- `benchmark/questions.jsonl`: câu hỏi, đáp án, gold source/page, evidence nguyên văn và filter khai báo trước; `splits.json` lưu ID dev/test; `freeze.json` khóa SHA-256 dữ liệu, config và mã pipeline trước chạy.
- `configs/strategies.json`: A 500 ký tự/overlap 50; B theo heading/đoạn tối đa 1.000 ký tự; C giống B, chỉ bật filter khi câu hỏi có yêu cầu. B và C dùng cùng cache vector.
- Model `BAAI/bge-small-en-v1.5`, ONNX quantized của Qdrant, 384 chiều, cosine. FastEmbed 0.7.4 gọi `passage_embed` / `query_embed`; adapter này không thêm instruction prefix cho model v1.5. Chi tiết fingerprints và các phiên bản nằm trong `results/environment_dev.json`.
- Qdrant local persistent, collection `python313_A`, `python313_B`, `python313_C` tại `results/qdrant/`; exact dense search do Qdrant thực hiện. Thư mục store/cache/model/venv được gitignore và tái tạo được.

Muốn tái tạo chuẩn hóa từ **snapshot đã nộp**, chạy `.venv/Scripts/python.exe scripts/prepare_corpus.py`, rồi `scripts/prepare_benchmark.py`; hai script giữ nguyên dữ liệu đã khóa khi đầu vào không đổi. Không xóa snapshot để lấy tài liệu trực tuyến mới rồi coi đó là cùng thí nghiệm. Một corpus/model/config mới cần thí nghiệm và holdout mới, công khai lịch sử.

## Artifact để chấm và đối chiếu

| Nội dung | Đường dẫn |
|---|---|
| Kết quả riêng dev/test | `results/metrics_dev.json`, `results/metrics_test.json` |
| Quyết định trước test | `results/selection.json` |
| Đầy đủ 60 lượt top-3 | `results/traces_dev.jsonl`, `results/traces_test.jsonl` |
| Chunk, vị trí và metadata | `results/chunks_A.jsonl`, `chunks_B.jsonl`, `chunks_C.jsonl` |
| Thời gian, độ dài, token, nạp lại | `results/ingestion_stats.json`, `token_statistics.json`, `persistence_check.json` |
| Evidence đã xác minh | `results/evidence_validation.json` |
| Mẫu và nhãn đánh giá | `results/coherence_anchors.json`, `results/audit_labels.json`, `results/audit_review.md` |
| Nhật ký cấu hình và giả thuyết | `artifacts/experiment_log.csv` |
| Kiểm tra bài nộp | `results/submission_check.json` |
| Tái lập trong store mới | `results/reproduction_check.json`, `results/reproduction_run.txt` |
| Evidence tương đương v2 | `results/evidence_review_v2.md`, `metrics_reviewed_dev.json`, `metrics_reviewed_test.json` |
| Học viên tự rà soát | `results/student_review.csv`, `results/human_review_status.json`, `docs/STUDENT_REVIEW.md` |

Kết quả gốc đo literal Hit@1/3: một chunk đúng nguồn/page chứa nguyên quote. Bản v2 bổ sung **evidence tương đương đủ ý trong một chunk**, có lý do từng record, không tính source-only hoặc union hai chunk. V2 sửa evaluation sau khi đã xem test, có cờ post-hoc/AI-assisted, giữ nguyên cấu hình/query/ranking và không chọn lại chiến lược; không được báo là accuracy tăng do cải tiến retrieval hay holdout mới. Nhãn coherence/grounding được đọc riêng, không suy từ Hit@3. Học viên cần tự đối chiếu các phán quyết trước khi nhận là nhãn do con người chấm.

`verify_submission.py` trả exit code 0 khi **kiểm tra kỹ thuật** đạt. Hãy đọc riêng `rubric_complete`, `submission_ready` và `pending_actions`; các trường này chưa hoàn tất khi còn review cá nhân, commit hoặc gửi link. Không diễn giải exit code 0 là đã hoàn tất toàn bộ rubric. Đối chiếu chi tiết tại [RUBRIC_AUDIT.md](RUBRIC_AUDIT.md), và làm phần cần tự xác nhận theo [STUDENT_REVIEW.md](STUDENT_REVIEW.md).

Bản `output/pdf/python-3.13-library.pdf` tải thêm từ trang chính thức chỉ để tham khảo. Corpus đã benchmark vẫn là 32 đơn vị HTML theo GUIDE; PDF không được cộng vào số trang corpus và chưa chạy thí nghiệm nào trên nó.

Chi phí embedding API bằng 0 USD; chưa quy đổi điện, máy, mạng hay thời gian. Các log thời gian là một lượt chạy trên máy này, không phải benchmark hiệu năng có nhiều lần lặp.

Trước khi nộp, rà soát báo cáo/nhãn, tạo commit và điền SHA trong STUDENT, kiểm tra quyền truy cập repo và tự gửi link qua kênh lớp. Việc push hoặc gửi bài chưa được thực hiện trong phiên này.
