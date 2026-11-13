"""Record judgments from direct reading of the ten preregistered source anchors.

Scores below are authored review decisions, NOT inferred from retrieval metrics.
Reviewer is Codex (AI); do not relabel as human-confirmed without student review.
"""
import json
from starter_import import ROOT
from starter.src.ingestion import load_jsonl
from starter.src.chunking import fixed_size, by_paragraph

DECISIONS = {
    "array": [(1, "Giữ được định nghĩa array và type code nhưng kết thúc giữa nhãn 'Minimum size in by'; bảng thiếu cấu trúc/tiêu đề đầy đủ."),
              (1, "Đoạn mở đầu và các type code đọc được, nhưng bảng đã trải phẳng và ghi chú 'It can be 16 bits or 32 bits' thiếu đối tượng/ghi chú kế tiếp; chưa tự đủ ngữ cảnh.")],
    "bisect": [(1, "Mục đích duy trì danh sách có thứ tự rõ, nhưng phần giải thích insertion point bị cắt ở 'this modul'."),
               (2, "Giữ trọn mục đích module và giải thích insertion point, so sánh __lt__ thay __eq__; nhãn Note ở cuối không làm mất ý chính.")],
    "codecs": [(1, "Có chủ thể module và chuyển đổi text/bytes, nhưng câu về custom codecs bị cắt ở 'arbi', thiếu giới hạn áp dụng."),
               (2, "Đủ định nghĩa registry, các kiểu chuyển đổi, giới hạn text encoding và mô tả encode; câu kết hoàn chỉnh.")],
    "collections": [(1, "Định nghĩa module rõ, nhưng bảng container bị cắt ngay phần Counter ('counting h'), khiến mục danh sách dang dở."),
                    (2, "Có tiêu đề, mục đích và đầy đủ tên/mô tả các container trong bảng mở đầu; có thể hiểu độc lập.")],
    "collections.abc": [(1, "Giới thiệu kiểm tra interface còn đủ, nhưng hướng dẫn kế thừa ABC bị cắt giữa từ ở 'one of th'."),
                        (1, "Định nghĩa interface rõ và có ví dụ kế thừa trực tiếp, nhưng câu báo có ba cách rồi chỉ trình bày cách đầu; ngữ cảnh hướng dẫn chưa đầy đủ.")],
    "configparser": [(2, "Đủ mục đích ConfigParser/INI và ngoại lệ value-type prefix; Module tomllib là tên tham chiếu, không làm sai hay cắt ý chính."),
                     (2, "Giữ trọn mô tả, giới hạn INI và ba lựa chọn TOML/shlex/JSON cùng giải thích; không cắt giữa câu.")],
    "copy": [(1, "Phân biệt assignment và copying rõ nhưng signature deepcopy bị cắt ngay '[, memo', chưa dùng được độc lập."),
             (1, "Có interface copy/deepcopy/replace/Error đầy đủ, nhưng câu cuối mở ra khác biệt shallow/deep với dấu hai chấm mà thiếu giải thích tiếp theo.")],
    "csv": [(1, "Có chủ thể CSV và lý do khác biệt định dạng, nhưng đoạn bị cắt trước lời giải thích vai trò module thống nhất I/O."),
            (2, "Trọn đoạn mở đầu: vấn đề thiếu chuẩn chung, khác delimiters/quoting và vai trò module che chi tiết đọc/ghi.")],
    "datetime": [(1, "Mục đích datetime hoàn chỉnh, nhưng phần tham chiếu zoneinfo bị cắt ở 'IANA time', thiếu nội dung kết."),
                 (2, "Mục đích, ưu tiên triển khai và các module/package tham chiếu đều được giữ trọn; không cần đoạn bên cạnh để hiểu.")],
    "decimal": [(1, "Giới thiệu số thập phân rõ nhưng trích dẫn lý do thiết kế dừng giữa từ 'excer', thiếu kết câu và ví dụ."),
                (2, "Giới thiệu, trích dẫn có nguồn và ví dụ 1.1+2.2 về sai số binary đều hoàn chỉnh; giữ mạch ý.")],
}


def main():
    pages={p.document_id:p for p in load_jsonl(ROOT/"data/pages.jsonl")}
    anchors=json.loads((ROOT/"results/coherence_anchors.json").read_text(encoding="utf-8"))
    rows=[]
    for strategy in "ABC":
        for anchor in anchors:
            page=pages[anchor["document_id"]]
            chunks=fixed_size(page,500,50) if strategy=="A" else by_paragraph(page,1000)
            chunk=min((c for c in chunks if c.metadata["char_start"]<=anchor["anchor"]<c.metadata["char_end"]),key=lambda c:c.metadata["char_start"])
            score,reason=DECISIONS[page.page][0 if strategy=="A" else 1]
            rows.append({"strategy":strategy, "document_id":page.document_id, "page":page.page,
                "anchor":anchor["anchor"], "chunk_id":chunk.chunk_id, "char_start":chunk.metadata["char_start"],
                "char_end":chunk.metadata["char_end"], "score":score,"reason":reason,
                "reviewer":"Codex — direct reading of source paragraph and selected chunk", "human_confirmed":False})
    (ROOT/"results/coherence_labels.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Recorded 30 directly reviewed coherence labels; human confirmation not asserted.")

if __name__=="__main__":
    main()
