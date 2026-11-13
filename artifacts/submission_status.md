# Đối chiếu bài nộp — Hà Huy Thái / 2A202603682 / 3A

Checklist này dẫn tới bằng chứng; không tự chấm điểm hay sửa checklist gốc trong SUBMISSION.md.

| Yêu cầu | Trạng thái và bằng chứng |
|---|---|
| Corpus ≥30 đơn vị nội dung có quyền xử lý | Đã có 32; `data/manifest.jsonl`, `pages.jsonl`, `raw/`, `LICENSE-PYTHON.txt`; không dùng số chunk làm số trang |
| Đọc, chuẩn hóa, log lỗi và truy nguồn | Đã chạy; `results/corpus_processing.jsonl`, `setup_notes.md`; chunk có URL/page/offset, không mất ký tự nội dung |
| Model embedding thật + persistent vector store | BGE ONNX 384 chiều + Qdrant local; model revision/SHA trong `data/model_manifest.json`; environment và kiểm tra persistence trong results |
| Ba cấu hình, so sánh có kiểm soát | `configs/strategies.json`, `artifacts/experiment_log.csv`; B/C cùng chunk/vector, chỉ khác filter |
| Nạp lại không trùng và tài liệu đổi | Upsert hai lần trong lượt thật giữ 2.017 / 1.151 / 1.151; test kiểm tra stale removal và reopen |
| ≥20 câu, dev/test trước chạy, evidence hợp lệ | 15 dev/5 test, 5 filter có 2 test; freeze/evidence_validation. V2 bổ sung equivalent evidence sau test, lưu riêng và chưa có học viên xác nhận |
| Trace và Hit@1/3 đủ ba cấu hình | 60 query/strategy traces, 180 hits; metrics_dev/test riêng; selection lưu trước test |
| Coherence | Đã trực tiếp đọc và ghi 30 nhãn AI hỗ trợ tại cùng 10 anchor, có lý do; **chưa có học viên xác nhận** |
| Metadata | Đã đọc/đối chiếu 45 records test; phân biệt đúng metadata và tuân filter, có lỗi phạm vi A/q19/rank3 |
| Grounding | Đã đọc 15 top-3 cases và ghi nhãn AI hỗ trợ, có lý do; **chưa có học viên xác nhận**; không nhận là độ chính xác chatbot |
| Data strategy impact và trade-off | Báo cáo có A–B/B–C, tài nguyên/cache, hồi quy q08, split q16, gold thiếu tương đương q20 và lỗi phạm vi q19 |
| Tái lập | `docs/RUNNING.md`, lock/model pin; 10 unit tests và 29 technical checks đạt; replay chạy thật vào store mới khớp 60 top-3 và giữ nguyên baseline |
| Báo cáo và thông tin học viên | `STUDENT.md`, `report/individual/2A202603682_HaHuyThai.md`, `docs/DEFENSE_NOTES.md` |
| Tệp yêu cầu gốc | RUBRIC/RULES/GUIDE/CHECKPOINTS/BENCHMARK/SUBMISSION/mẫu báo cáo không đổi; verifier kiểm tra bằng Git |

Trước khi nộp chính thức, học viên thực hiện các bước thuộc trách nhiệm cá nhân:

- [ ] Đọc và hiểu mã/báo cáo; đối chiếu nhãn trong `results/audit_review.md` với nguồn, chỉnh nhãn nếu cần và ghi việc tự xác nhận. Hiện không có nhãn giả mạo người chấm.
- [ ] Tạo commit chốt bài và điền SHA vào STUDENT.md; kiểm tra không đưa venv/model/cache/secret vào commit.
- [ ] Push repo cá nhân, bảo đảm người chấm truy cập được và gửi link theo kênh lớp. Chưa đánh dấu các hành động bên ngoài này là đã thực hiện.

Metric literal và tham số gốc giữ nguyên. Đã thêm equivalent-evidence v2 với lý do từng record; có cờ post-hoc/AI-assisted và không chọn lại chiến lược, không coi là holdout mới. Verifier tách kiểm tra kỹ thuật khỏi rubric_complete/submission_ready. Xem `docs/RUBRIC_AUDIT.md` để biết các điểm đã sửa và phần học viên cần tự làm; không lấy 29 checks đạt để tự nhận toàn bộ rubric hoàn chỉnh.
