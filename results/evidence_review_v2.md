# Evidence review v2 — đánh giá AI hỗ trợ sau thí nghiệm

All distinct A/B top-3 records read directly against question requirements and source. Literal positives retained; equivalent evidence accepted only in a single source-traceable chunk. Identical C material explicitly checked, not independently rejudged.

Giữ nguyên bộ câu hỏi, tham số, ranking, kết quả literal và lựa chọn C. Đây là sửa phép đánh giá sau khi đã thấy test, không phải holdout mới và chưa có con người xác nhận.

## q01

Template.is_valid returns False for invalid placeholders; do not confuse substitute raising an exception.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | string:28351 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 2 | string:29250 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |
| A | 3 | string:27000 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |
| B | 1 | string:27844 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | string:31411 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |
| B | 3 | string:29624 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |
| C | 1 | string:27844 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | string:31411 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |
| C | 3 | string:29624 | False | False | Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders. |

## q02

Raw strings preserve backslashes; raw backslash-n has two characters, unlike an ordinary newline literal.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | re:1350 | False | True | Có đủ bảo toàn backslash và raw backslash-n hai ký tự; phần mở đầu bị cắt không làm mất hai facts cần trả lời. |
| A | 2 | re:901 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |
| A | 3 | re:8550 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |
| B | 1 | re:1298 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | re:60178 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |
| B | 3 | re:8439 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |
| C | 1 | re:1298 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | re:60178 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |
| C | 3 | re:8439 | False | False | Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string. |

## q03

The default junk threshold concerns the second sequence, length >=200 and frequency >1%.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | difflib:451 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |
| A | 2 | difflib:1351 | False | True | Câu By default nêu chính second input sequence, ngưỡng ít nhất 200 và hơn 1%; phần cảnh báo bất đối xứng dài hơn trong gold không cần để trả lời ba facts này. |
| A | 3 | difflib:900 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |
| B | 1 | difflib:630 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | difflib:1747 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |
| B | 3 | difflib:15456 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |
| C | 1 | difflib:630 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | difflib:1747 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |
| C | 3 | difflib:15456 | False | False | Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk. |

## q04

For dedent, tab and space are not equal common indentation; generic TextWrapper tab expansion is insufficient.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | textwrap:2250 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |
| A | 2 | textwrap:2700 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 3 | textwrap:5850 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |
| B | 1 | textwrap:2670 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | textwrap:1760 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |
| B | 3 | textwrap:5365 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |
| C | 1 | textwrap:2670 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | textwrap:1760 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |
| C | 3 | textwrap:5365 | False | False | Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation. |

## q05

NFKD compatibility decomposition versus NFKC compatibility decomposition followed by canonical composition.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | unicodedata:3600 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| A | 2 | unicodedata:4050 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| A | 3 | unicodedata:5400 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| B | 1 | unicodedata:3717 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| B | 2 | unicodedata:5462 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| B | 3 | unicodedata:4489 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 1 | unicodedata:3717 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| C | 2 | unicodedata:5462 | False | False | Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk. |
| C | 3 | unicodedata:4489 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |

## q06

No struct prefix defaults to native mode, with padding for native C alignment.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | struct:5850 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |
| A | 2 | struct:450 | False | True | Có trọn điều kiện không prefix → native, platform/compiler và pad bytes giữ C alignment; phần contrast external sources bị cắt không thuộc câu hỏi. |
| A | 3 | struct:16650 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |
| B | 1 | struct:5850 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |
| B | 2 | struct:478 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 3 | struct:11849 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |
| C | 1 | struct:5850 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |
| C | 2 | struct:478 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 3 | struct:11849 | False | False | Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding. |

## q07

utf-8-sig writes ef bb bf and skips those bytes only when at the start of input.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | codecs:35101 | False | True | Nêu nguyên bộ byte ef/bb/bf lúc encode và chỉ skip khi là ba byte đầu lúc decode; không cần toàn đoạn giới thiệu BOM dài hơn của gold. |
| A | 2 | codecs:50850 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |
| A | 3 | codecs:33750 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |
| B | 1 | codecs:34849 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | codecs:50778 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |
| B | 3 | codecs:33156 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |
| C | 1 | codecs:34849 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | codecs:50778 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |
| C | 3 | codecs:33156 | False | False | Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input. |

## q08

Counter lookup of an absent key returns zero instead of KeyError; Counter equality/defaultdict are different operations.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | collections:8551 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 2 | string:4500 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| A | 3 | collections:24750 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| B | 1 | collections:23309 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| B | 2 | collections:10759 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| B | 3 | bisect:7780 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| C | 1 | collections:23309 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| C | 2 | collections:10759 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |
| C | 3 | bisect:7780 | False | False | Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup. |

## q09

Appending to a full bounded deque discards corresponding items from the opposite end.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | collections:15750 | False | True | Có nguyên điều kiện deque đầy/bounded và discarded corresponding items from opposite end; câu tail-filter sau đó không cần cho đáp án. |
| A | 2 | collections:18901 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |
| A | 3 | collections:16200 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |
| B | 1 | collections:15925 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | collections:15160 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |
| B | 3 | collections:18897 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |
| C | 1 | collections:15925 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | collections:15160 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |
| C | 3 | collections:18897 | False | False | Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk. |

## q10

heap[0] accesses minimum without popping; heappop of an empty heap raises IndexError (not only heapreplace).

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | heapq:1800 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |
| A | 2 | heapq:901 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |
| A | 3 | heapq:1350 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 1 | heapq:1631 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | heapq:638 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |
| B | 3 | heapq:8167 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |
| C | 1 | heapq:1631 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | heapq:638 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |
| C | 3 | heapq:8167 | False | False | Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk. |

## q11

Concurrent mutation/use of bisect/insort on the same sequence is unsafe/undefined and may leave it unsorted.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | bisect:901 | False | True | Có câu mutating same sequence while bisect operates → undefined và ví dụ concurrent insort_left làm list unsorted; trả lời trực tiếp điều kiện đồng thời trong query. |
| A | 2 | bisect:4051 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |
| A | 3 | bisect:4501 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |
| B | 1 | bisect:770 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | bisect:4029 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |
| B | 3 | bisect:5205 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |
| C | 1 | bisect:770 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | bisect:4029 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |
| C | 3 | bisect:5205 | False | False | Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition. |

## q12

deepcopy uses a memo dictionary of already-copied objects in the current pass; a bare memo argument is insufficient.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | copy:1350 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 2 | pickle:39152 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |
| A | 3 | copy:450 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |
| B | 1 | copy:905 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | copy:2739 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |
| B | 3 | copy:0 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |
| C | 1 | copy:905 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | copy:2739 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |
| C | 3 | copy:0 | False | False | Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass. |

## q13

datetime awareness requires tzinfo not None AND tzinfo.utcoffset(d) not None.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | datetime:4500 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 2 | datetime:52650 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |
| A | 3 | datetime:40950 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |
| B | 1 | datetime:4388 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | datetime:765 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |
| B | 3 | datetime:35049 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |
| C | 1 | datetime:4388 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | datetime:765 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |
| C | 3 | datetime:35049 | False | False | Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset. |

## q14

Decimal(float) retains the binary float approximation exactly rather than rounding it away; an explicit constructor example can demonstrate this.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | decimal:4950 | False | True | Ví dụ Decimal(3.14) cho đầy đủ các chữ số của binary approximation trong khi Decimal('3.14') giữ 3.14; trực tiếp phân biệt hai hành vi câu hỏi. |
| A | 2 | decimal:40050 | False | False | Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion. |
| A | 3 | decimal:19800 | False | True | Nêu Decimal.from_float(0.1) khác Decimal('0.1'), giá trị nhị phân gần nhất và decimal tương đương; không đòi literal quote của đoạn primer. |
| B | 1 | decimal:39357 | False | False | Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion. |
| B | 2 | string:20421 | False | False | Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion. |
| B | 3 | decimal:4898 | False | True | Ví dụ constructor Decimal(3.14) giữ đầy đủ sai số biểu diễn float, khác Decimal('3.14'); đủ evidence tương đương trên cùng trang. |
| C | 1 | decimal:39357 | False | False | Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion. |
| C | 2 | string:20421 | False | False | Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion. |
| C | 3 | decimal:4898 | False | True | Ví dụ constructor Decimal(3.14) giữ đầy đủ sai số biểu diễn float, khác Decimal('3.14'); đủ evidence tương đương trên cùng trang. |

## q15

harmonic_mean exits early on zero without validating subsequent inputs; result-is-zero alone is insufficient.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | statistics:6301 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| A | 2 | decimal:56251 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| A | 3 | statistics:5850 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| B | 1 | statistics:7180 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | decimal:25797 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| B | 3 | statistics:6188 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| C | 1 | statistics:7180 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | decimal:25797 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |
| C | 3 | statistics:6188 | False | False | Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs. |

## q16

Path.resolve in this 3.13 snapshot raises OSError for a missing path/loop in strict mode, otherwise resolves as far as possible and appends the unchecked remainder. A historical change note is not additionally required to answer current behavior.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | pathlib:24750 | False | True | Đoạn chính trong snapshot 3.13 giữ đủ cả missing path/symlink loop, strict OSError và non-strict resolve/append; không cần note lịch sử để trả lời behavior hiện tại. |
| A | 2 | os.path:13501 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |
| A | 3 | pathlib:10350 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |
| B | 1 | os.path:13799 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |
| B | 2 | pathlib:24388 | False | True | Cùng một chunk chứa signature Path.resolve và toàn đoạn strict/non-strict cho missing path/loop; đủ current behavior dù note lịch sử 3.13 ở chunk kế tiếp. |
| B | 3 | pathlib:25193 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |
| C | 1 | os.path:13799 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |
| C | 2 | pathlib:24388 | False | True | Cùng một chunk chứa signature Path.resolve và toàn đoạn strict/non-strict cho missing path/loop; đủ current behavior dù note lịch sử 3.13 ở chunk kế tiếp. |
| C | 3 | pathlib:25193 | False | False | Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk. |

## q17

commonprefix operates character by character and can return invalid paths; use commonpath.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | os.path:3601 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |
| A | 2 | os.path:2700 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |
| A | 3 | os.path:3150 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 1 | os.path:2747 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | os.path:3610 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |
| B | 3 | os.path:13799 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |
| C | 1 | os.path:2747 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | os.path:3610 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |
| C | 3 | os.path:13799 | False | False | Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi. |

## q18

Given Windows/delete=True/delete_on_close=False supplied in the question, additional opens not sharing delete access must close before context exit, or unlink raises PermissionError.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | tempfile:4950 | False | True | Question đã cho Windows và delete flags; chunk giữ điều kiện delete_on_close=False, additional opens không share delete access, phải đóng trước exit và hậu quả PermissionError. Không dùng union hai chunk để tính hit. |
| A | 2 | tempfile:4500 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |
| A | 3 | tempfile:5400 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |
| B | 1 | tempfile:4746 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | tempfile:3788 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |
| B | 3 | tempfile:7862 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |
| C | 1 | tempfile:4746 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | tempfile:3788 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |
| C | 3 | tempfile:7862 | False | False | Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk. |

## q19

newline='' avoids misinterpreted embedded quoted newlines and an extra carriage return on CRLF writes; csv handles newlines itself.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | csv:20250 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |
| A | 2 | csv:21150 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| A | 3 | difflib:13051 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |
| B | 1 | csv:21215 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| B | 2 | csv:20362 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |
| B | 3 | csv:3092 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |
| C | 1 | csv:21215 | True | False | Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy. |
| C | 2 | csv:20362 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |
| C | 3 | csv:3092 | False | False | Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning. |

## q20

Affirmative instruction or concrete SQL example binds values using placeholders and separate execute parameters, rather than interpolating SQL strings. A heading/warning alone is insufficient.

| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |
|---|---:|---|---|---|---|
| A | 1 | sqlite3:53550 | False | False | Chỉ có heading/cảnh báo injection; không có affirmative binding instruction hoặc parameterized example hoàn chỉnh. |
| A | 2 | sqlite3:39600 | False | True | Mô tả execute(sql, parameters), binding Python values using placeholders, và dict/sequence parameters đầy đủ; đây là affirmative binding instruction trên trang sqlite3. |
| A | 3 | sqlite3:59400 | False | True | Ví dụ execute INSERT ... VALUES(?) với tuple (p,) truyền riêng minh họa đúng parameter binding; không dựa vào phép ghép chuỗi hay đoạn gold duy nhất. |
| B | 1 | sqlite3:53718 | False | True | Đủ cảnh báo string interpolation/SQL injection và hướng dẫn Instead use parameter substitution, placeholder, tuple làm argument thứ hai của execute. |
| B | 2 | sqlite3:63235 | False | True | Code execute INSERT ... VALUES(?) với tuple ('Python',) truyền riêng là bằng chứng parameter binding hợp lệ, dù mục gốc bàn transaction context. |
| B | 3 | sqlite3:41127 | False | True | Code executemany INSERT ... VALUES(?) với rows tuples thể hiện parameter binding an toàn cho nhiều SQL rows; không cần literal quote của primer. |
| C | 1 | sqlite3:53718 | False | True | Đủ cảnh báo string interpolation/SQL injection và hướng dẫn Instead use parameter substitution, placeholder, tuple làm argument thứ hai của execute. |
| C | 2 | sqlite3:63235 | False | True | Code execute INSERT ... VALUES(?) với tuple ('Python',) truyền riêng là bằng chứng parameter binding hợp lệ, dù mục gốc bàn transaction context. |
| C | 3 | sqlite3:41127 | False | True | Code executemany INSERT ... VALUES(?) với rows tuples thể hiện parameter binding an toàn cho nhiều SQL rows; không cần literal quote của primer. |

