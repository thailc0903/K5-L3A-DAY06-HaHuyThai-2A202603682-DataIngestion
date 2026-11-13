"""Materialize authored questions and exact, source-verified evidence BEFORE retrieval."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    pages = {p["page"]: p for p in map(json.loads, (ROOT / "data/pages.jsonl").read_text(encoding="utf-8").splitlines())}
    records = []

    def add(module, question, answer, indices, kind="direct", filtered=False, substring=None):
        page = pages[module]
        paragraphs = page["text"].split("\n\n")
        quote = "\n\n".join(paragraphs[a] for a in indices)
        assert quote in page["text"], (module, indices)
        if substring:
            assert substring in quote
            quote = substring
        split = "dev" if len(records) < 15 else "test"
        category = page["metadata"]["category"]
        if filtered:
            question = f"User context: restrict retrieval to the official chapter '{category}'. " + question
        records.append({"id": f"q{len(records)+1:02d}", "split": split, "type": kind,
            "question": question, "expected_answer": answer,
            "gold_source_id": page["document_id"], "gold_page": module, "evidence_quote": quote,
            "filter": {"category": category} if filtered else {},
            "filter_origin": "Explicit user-context chapter in question, declared before retrieval" if filtered else None,
            "alternative_gold": [], "evidence_verified": True})

    add("string", "What does Template.is_valid() return when a template contains invalid placeholders?",
        "False; those invalid placeholders would make substitute() raise ValueError.", [213,214])
    add("re", 'Why is the raw-string spelling r"\\n" useful for a regex, and how many characters does that Python string contain?',
        "Raw strings do not handle backslashes specially; it contains two characters, a backslash and n, whereas the ordinary literal contains one newline.", [5], filtered=True)
    add("difflib", "For SequenceMatcher's default junk heuristic, which sequence is inspected and what length and frequency thresholds apply?",
        "Only the second sequence is inspected. If it has at least 200 items, items accounting for more than 1% are treated as junk.", [8,9], "conditional")
    add("textwrap", 'When dedenting text, do a leading space and a leading tab count as the same common indentation?',
        'No. Tabs and spaces are whitespace but not equal, so " hello" and "\\thello" have no common leading whitespace.', [20], "paraphrase")
    add("unicodedata", "In Unicode normalization, what operations distinguish NFKD from NFKC?",
        "NFKD applies compatibility decomposition. NFKC applies compatibility decomposition followed by canonical composition.", [44])
    add("struct", "What mode does struct use if a format string has no prefix, and what happens to alignment padding?",
        "Native mode, based on the interpreter's platform/compiler; padding bytes maintain C type alignment in packing and unpacking.", [4], "conditional", True)
    add("codecs", "For utf-8-sig, which three bytes are written at the start on encoding and when are they skipped on decoding?",
        "0xef, 0xbb, 0xbf are written first. They are skipped on decoding only if they are the first three bytes; a UTF-8 BOM is generally discouraged.", [286], "conditional", True)
    add("collections", "Does looking up an absent item in a Counter raise KeyError?",
        "No. Counter returns a zero count for a missing item.", [68], "paraphrase")
    add("collections", "What happens at the opposite end when new items are appended to an already full bounded deque?",
        "A corresponding number of items are discarded from the opposite end; maxlen bounds the deque.", [127], "conditional")
    add("heapq", "Which heap list position gives the smallest item without removing it, and what does heappop do on an empty heap?",
        "heap[0] gives the smallest item without popping. heappop raises IndexError if the heap is empty.", [14], "conditional")
    add("bisect", "Can several threads safely run bisect or insort_left on the same list while another thread mutates it?",
        "No. These functions are not thread-safe; concurrent use or mutation can have undefined behavior, and insort_left may leave the list unsorted.", [5], "conditional")
    add("copy", "What bookkeeping mechanism does deepcopy use to avoid repeated copying of objects during the current pass?",
        "It keeps a memo dictionary of objects already copied during the current copying pass.", [19,20], "paraphrase")
    add("datetime", "What two conditions must hold for a datetime object d to be aware rather than naive?",
        "d.tzinfo is not None, and d.tzinfo.utcoffset(d) does not return None. Otherwise d is naive.", list(range(57,61)), "conditional")
    add("decimal", "Does constructing Decimal from a float round away the float representation error, or exactly convert the float value?",
        "Construction performs an exact conversion of the float's value; using a decimal string avoids importing an existing binary floating-point approximation.", [21], "paraphrase")
    add("statistics", "Does harmonic_mean validate every subsequent input after it encounters a zero?",
        "No. The current algorithm exits early on zero, so later inputs are not tested for validity; this may change in future.", [90], "conditional")
    # Reserved module topics for holdout. Never use their retrieval scores to tune.
    add("pathlib", "In Python 3.13, how does Path.resolve handle a nonexistent path or symlink loop with strict=True versus strict=False?",
        "Strict mode raises OSError. Non-strict mode resolves as far as possible and appends the remainder without existence checks; symlink loops follow the same strict/non-strict error policy in 3.13.", [243,244,245], "conditional", True)
    add("os.path", "Why can commonprefix return an invalid filesystem path, and which function should be used to find a common path prefix?",
        "It works character by character and can return invalid paths; use commonpath for a common path prefix.", [31], "paraphrase")
    add("tempfile", "On Windows, when reopening a NamedTemporaryFile with delete=True and delete_on_close=False through builtin open, what must happen before context-manager exit?",
        "Additional opens that do not share delete access must be closed before exiting; otherwise os.unlink on exit raises PermissionError.", [25,26,27,28], "conditional")
    add("csv", "Why should CSV files be opened with newline='' when fields can contain newlines or a platform writes CRLF?",
        "Without it, embedded newlines in quoted fields are not interpreted correctly and CRLF platforms may add an extra carriage return on write; csv handles newline translation itself.", [181], "conditional", True)
    add("sqlite3", "How should Python values be bound into sqlite3 SQL statements to avoid SQL injection?",
        "Use placeholders, such as ?, to bind values instead of string formatting.", [38], "direct")
    assert len(records) == 20
    target = ROOT / "benchmark"
    target.mkdir(exist_ok=True)
    (target / "questions.jsonl").write_text("".join(json.dumps(q, ensure_ascii=False) + "\n" for q in records), encoding="utf-8")
    (target / "splits.json").write_text(json.dumps({split: [q["id"] for q in records if q["split"] == split] for split in ["dev", "test"]}, indent=2) + "\n")
    readable=["# Bộ câu hỏi và gold evidence", "", "Bản đọc thuận tiện của questions.jsonl đã khóa; không phải thay đổi BENCHMARK.md. Evidence được xác minh trên snapshot trước retrieval.", ""]
    for q in records:
        readable.extend([f"## {q['id']} · {q['split']} · {q['type']}", "", q["question"], "",
            "**Đáp án cần hỗ trợ:** "+q["expected_answer"], "",
            f"**Nguồn/page:** [{q['gold_source_id']} / {q['gold_page']}]({pages[q['gold_page']]['source']})", "",
            "**Filter trước truy xuất:** "+json.dumps(q["filter"],ensure_ascii=False), "", "~~~text", q["evidence_quote"], "~~~", ""])
    (target / "questions.md").write_text("\n".join(readable)+"\n",encoding="utf-8")
    print("Authored and source-verified 15 dev + 5 test questions; 5 filters (including 2 test).")

if __name__ == "__main__":
    main()
