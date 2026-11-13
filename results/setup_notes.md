# Nhật ký thiết lập và giới hạn môi trường

- Ban đầu PowerShell không có `python` trên PATH, Docker không hiện trong `Get-Command`. Đã dùng `uv` để tải CPython 3.12.16 vào `.runtime/python`, tạo `.venv` trong repo. Không đổi cấu hình Python toàn máy.
- Lượt tải Python đầu trong sandbox thất bại với WinError 10013 (socket bị hạn chế). Lượt được cấp quyền mạng đã thành công; không dùng runtime giả.
- Cài dependencies bằng `uv pip install` từ PyPI có lượt treo trong khi tải wheel lớn. Đã dừng đúng tiến trình cài do phiên này tạo và thử tải tuần tự; tiếp đó tải wheel theo HTTP Range, đối chiếu SHA-256 của từng wheel với JSON chính thức từ PyPI. `requirements.lock` lưu các phiên bản được resolver chọn.
- Lượt chuẩn bị corpus đầu dừng do giả định sai rằng `fileinput` thuộc chương File and Directory Access. Kiểm tra các link chapter chính thức cho thấy không có module đó; đã chọn `filecmp`, thuộc đúng chương. Lỗi AssertionError và các đơn vị đọc được vẫn được giữ trong `corpus_processing.jsonl`. Sửa này xảy ra **trước** chốt benchmark và trước retrieval.
- Không có dữ liệu cá nhân của bên thứ ba, secret, API key hay dịch vụ trả phí trong corpus. Thông tin học viên được chính học viên cung cấp cho STUDENT và báo cáo.
- Ngày giờ artifact lưu UTC có offset; ngày dùng trong báo cáo theo Asia/Saigon. Thời gian đo bằng `perf_counter`, không suy ra từ checkpoint 4 giờ.
