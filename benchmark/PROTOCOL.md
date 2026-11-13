# Giao thức chốt trước thí nghiệm

AI hỗ trợ chuẩn bị và kiểm tra; không giả mạo người chấm hay số liệu.

- Corpus: các trang tham chiếu module độc lập của Python 3.13, tiếng Anh. Mỗi đơn vị ≥1.500 ký tự sau chuẩn hóa; không coi một chunk là một trang. Lưu bản HTML, giấy phép và SHA-256.
- Benchmark gồm đúng 20 câu tiếng Anh để kiểm tra retrieval cùng ngôn ngữ corpus. 15 dev tập trung text/binary/data types/numeric; 5 test dành cho filesystem/file formats/persistence. Chia theo module, không đặt cùng module gold ở cả hai split. Không hứa tính độc lập tuyệt đối: cùng bộ tài liệu và các API có tham chiếu chéo; người xây benchmark biết trước gold.
- Tối thiểu ba câu filter, gồm câu test. `category` là tên chương chính thức trên trang chapter; câu hỏi ghi ngữ cảnh chương trước truy xuất. Đây là user-context input, không suy filter từ gold sau truy xuất. Không lọc `document_id` hoặc page.
- Giữ nguyên model, corpus, bộ câu hỏi, cosine và top-3. A fixed 500/overlap 50; B paragraph/heading tối đa 1.000 ký tự; C cùng chunk và vector như B, chỉ bật filter khi câu hỏi yêu cầu.
- Chọn trên dev: Evidence Hit@3 → Hit@1 → ít tổng ký tự lưu hơn → thứ tự ưu tiên C, B, A khi hòa hoàn toàn. Không dùng test để chỉnh chunk/model/query/filter.
- Một hit cần đúng source_id + page và toàn bộ evidence trong **một chunk**. Gold thay thế khai báo trước được chấp nhận. Không dùng source-only hit, không gộp nhiều chunk để nâng metric chính.
- Freeze SHA-256 corpus, benchmark, config và code trước embedding/truy xuất. `selection.json` phải được lưu trước `traces_test.jsonl`. Chạy lại cùng cấu hình là tái lập, không phải một holdout mới.
- Coherence: 10 source_id đầu theo thứ tự chữ cái; chọn giữa đoạn văn đầu dài ≥150 ký tự. Với nhiều chunk phủ anchor, lấy chunk có char_start nhỏ nhất. Chốt anchor trước điểm retrieval; dùng cùng anchor A/B/C.
- Grounding: đọc đủ 5 test × 3 chiến lược; thang 0 thiếu bằng chứng, 1 có nhưng thiếu điều kiện/ngữ cảnh, 2 đủ và truy nguồn. Metadata: đối chiếu đủ 45 top-3 records với nguồn. Không suy hai nhãn này chỉ từ Hit@3.
- Nhãn do Codex đọc trực tiếp phải ghi là đánh giá AI hỗ trợ; học viên cần rà soát và xác nhận trước khi nhận là nhãn do con người chấm. Báo cáo công khai hạn chế và thiên lệch.
- Ghi lỗi provider/setup, thời gian, phiên bản, fingerprint model và chi phí API thực. Local API cost = 0 USD không có nghĩa toàn bộ chi phí vận hành bằng 0.
