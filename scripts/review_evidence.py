"""Versioned post-retrieval evidence review; original benchmark/results stay frozen.

Judgments below record direct reading of all distinct A/B top-3 texts in the
rubric audit. C is reused only when its exact ranked texts match B. These are
disclosed AI-assisted judgments, not human-confirmed labels or fresh holdout data.
"""
import copy
import hashlib
import json
from datetime import datetime, timezone
try:
    from .starter_import import ROOT
except ImportError:
    from starter_import import ROOT
from starter.src.evaluation import summarize

REQUIREMENTS = {
    "q01": "Template.is_valid returns False for invalid placeholders; do not confuse substitute raising an exception.",
    "q02": "Raw strings preserve backslashes; raw backslash-n has two characters, unlike an ordinary newline literal.",
    "q03": "The default junk threshold concerns the second sequence, length >=200 and frequency >1%.",
    "q04": "For dedent, tab and space are not equal common indentation; generic TextWrapper tab expansion is insufficient.",
    "q05": "NFKD compatibility decomposition versus NFKC compatibility decomposition followed by canonical composition.",
    "q06": "No struct prefix defaults to native mode, with padding for native C alignment.",
    "q07": "utf-8-sig writes ef bb bf and skips those bytes only when at the start of input.",
    "q08": "Counter lookup of an absent key returns zero instead of KeyError; Counter equality/defaultdict are different operations.",
    "q09": "Appending to a full bounded deque discards corresponding items from the opposite end.",
    "q10": "heap[0] accesses minimum without popping; heappop of an empty heap raises IndexError (not only heapreplace).",
    "q11": "Concurrent mutation/use of bisect/insort on the same sequence is unsafe/undefined and may leave it unsorted.",
    "q12": "deepcopy uses a memo dictionary of already-copied objects in the current pass; a bare memo argument is insufficient.",
    "q13": "datetime awareness requires tzinfo not None AND tzinfo.utcoffset(d) not None.",
    "q14": "Decimal(float) retains the binary float approximation exactly rather than rounding it away; an explicit constructor example can demonstrate this.",
    "q15": "harmonic_mean exits early on zero without validating subsequent inputs; result-is-zero alone is insufficient.",
    "q16": "Path.resolve in this 3.13 snapshot raises OSError for a missing path/loop in strict mode, otherwise resolves as far as possible and appends the unchecked remainder. A historical change note is not additionally required to answer current behavior.",
    "q17": "commonprefix operates character by character and can return invalid paths; use commonpath.",
    "q18": "Given Windows/delete=True/delete_on_close=False supplied in the question, additional opens not sharing delete access must close before context exit, or unlink raises PermissionError.",
    "q19": "newline='' avoids misinterpreted embedded quoted newlines and an extra carriage return on CRLF writes; csv handles newlines itself.",
    "q20": "Affirmative instruction or concrete SQL example binds values using placeholders and separate execute parameters, rather than interpolating SQL strings. A heading/warning alone is insufficient.",
}

# (strategy, question, rank): (reviewed source offset, reason). Never select a
# different chunk: these offsets identify the already-saved retrieval records.
EXTRA = {
    ("A","q02",1):(1350,"Có đủ bảo toàn backslash và raw backslash-n hai ký tự; phần mở đầu bị cắt không làm mất hai facts cần trả lời."),
    ("A","q03",2):(1351,"Câu By default nêu chính second input sequence, ngưỡng ít nhất 200 và hơn 1%; phần cảnh báo bất đối xứng dài hơn trong gold không cần để trả lời ba facts này."),
    ("A","q06",2):(450,"Có trọn điều kiện không prefix → native, platform/compiler và pad bytes giữ C alignment; phần contrast external sources bị cắt không thuộc câu hỏi."),
    ("A","q07",1):(35101,"Nêu nguyên bộ byte ef/bb/bf lúc encode và chỉ skip khi là ba byte đầu lúc decode; không cần toàn đoạn giới thiệu BOM dài hơn của gold."),
    ("A","q09",1):(15750,"Có nguyên điều kiện deque đầy/bounded và discarded corresponding items from opposite end; câu tail-filter sau đó không cần cho đáp án."),
    ("A","q11",1):(901,"Có câu mutating same sequence while bisect operates → undefined và ví dụ concurrent insort_left làm list unsorted; trả lời trực tiếp điều kiện đồng thời trong query."),
    ("A","q14",1):(4950,"Ví dụ Decimal(3.14) cho đầy đủ các chữ số của binary approximation trong khi Decimal('3.14') giữ 3.14; trực tiếp phân biệt hai hành vi câu hỏi."),
    ("A","q14",3):(19800,"Nêu Decimal.from_float(0.1) khác Decimal('0.1'), giá trị nhị phân gần nhất và decimal tương đương; không đòi literal quote của đoạn primer."),
    ("B","q14",3):(4898,"Ví dụ constructor Decimal(3.14) giữ đầy đủ sai số biểu diễn float, khác Decimal('3.14'); đủ evidence tương đương trên cùng trang."),
    ("A","q16",1):(24750,"Đoạn chính trong snapshot 3.13 giữ đủ cả missing path/symlink loop, strict OSError và non-strict resolve/append; không cần note lịch sử để trả lời behavior hiện tại."),
    ("B","q16",2):(24388,"Cùng một chunk chứa signature Path.resolve và toàn đoạn strict/non-strict cho missing path/loop; đủ current behavior dù note lịch sử 3.13 ở chunk kế tiếp."),
    ("A","q18",1):(4950,"Question đã cho Windows và delete flags; chunk giữ điều kiện delete_on_close=False, additional opens không share delete access, phải đóng trước exit và hậu quả PermissionError. Không dùng union hai chunk để tính hit."),
    ("A","q20",2):(39600,"Mô tả execute(sql, parameters), binding Python values using placeholders, và dict/sequence parameters đầy đủ; đây là affirmative binding instruction trên trang sqlite3."),
    ("A","q20",3):(59400,"Ví dụ execute INSERT ... VALUES(?) với tuple (p,) truyền riêng minh họa đúng parameter binding; không dựa vào phép ghép chuỗi hay đoạn gold duy nhất."),
    ("B","q20",1):(53718,"Đủ cảnh báo string interpolation/SQL injection và hướng dẫn Instead use parameter substitution, placeholder, tuple làm argument thứ hai của execute."),
    ("B","q20",2):(63235,"Code execute INSERT ... VALUES(?) với tuple ('Python',) truyền riêng là bằng chứng parameter binding hợp lệ, dù mục gốc bàn transaction context."),
    ("B","q20",3):(41127,"Code executemany INSERT ... VALUES(?) với rows tuples thể hiện parameter binding an toàn cho nhiều SQL rows; không cần literal quote của primer."),
}

NEGATIVE = {
    "q01":"Bàn substitute, delimiter hoặc customization, không khẳng định kết quả is_valid cho invalid placeholders.",
    "q02":"Chỉ nói escape/backslash hoặc ví dụ regex khác, chưa đủ cả raw backslash-n có hai ký tự và cơ chế raw string.",
    "q03":"Chỉ có mô tả thuật toán/asymmetry/constructor, thiếu ngưỡng length>=200 và >1% cùng phạm vi second sequence trong một chunk.",
    "q04":"Mô tả dedent chung hoặc TextWrapper tab expansion; thiếu khẳng định tab và space không equal trong common indentation.",
    "q05":"Chỉ nêu danh sách normal forms hoặc fragment composition; thiếu so sánh đầy đủ NFKD/NFKC trong một chunk.",
    "q06":"Chỉ có padding notes hoặc native examples, không đủ đồng thời default-no-prefix và C alignment padding.",
    "q07":"Chỉ nói BOM/UTF-8 chung; chưa đủ cả ba byte cụ thể và điều kiện skip ở đầu input.",
    "q08":"Nói defaultdict/formatting/bisect hoặc Counter comparison; không chứng minh hành vi Counter missing-key lookup.",
    "q09":"Chỉ có append/pop không bounded-full hoặc tail-filter context; không đủ điều kiện và discard-opposite-end trong một chunk.",
    "q10":"Nói heap minimum/invariant hoặc heapreplace; chưa đủ riêng heappop(empty) và truy cập không pop trong cùng một chunk.",
    "q11":"Nói hiệu năng, caching key hoặc searching sorted list; không có thread-safety/concurrent mutation condition.",
    "q12":"Chỉ có signature/memo argument hoặc copying API; không nêu memo lưu các object đã copy trong current pass.",
    "q13":"Nói timezone/aware comparisons hoặc UTC conversion; không có đủ hai điều kiện tzinfo và utcoffset.",
    "q14":"Nói context-based rounding hoặc string formatting, là API khác với Decimal(float); không đủ constructor exact conversion.",
    "q15":"Chỉ nêu kết quả harmonic mean bằng zero/định nghĩa hoặc decimal/geometric_mean khác; không nói bỏ kiểm tra subsequent inputs.",
    "q16":"Nói os.path API khác, PurePath attributes hoặc chỉ note loop change; chưa đủ Path.resolve missing-path và cả strict/non-strict trong một chunk.",
    "q17":"Chỉ ví dụ commonprefix/commonpath, commonpath validity hoặc path API khác; thiếu giải thích character-by-character cần cho câu hỏi.",
    "q18":"Nói reopen possibilities/delete timing/POSIX/TemporaryDirectory; thiếu complete close-additional-opens-before-exit obligation và hậu quả trong một chunk.",
    "q19":"Chỉ có opening examples/encoding/dialect/difflib; thiếu cả embedded quoted newline và extra carriage return reasoning.",
    "q20":"Chỉ có heading/cảnh báo injection; không có affirmative binding instruction hoặc parameterized example hoàn chỉnh.",
}


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_review(traces):
    indexed={(t["strategy"],t["question_id"]):t for t in traces}
    pages={(p["document_id"],p["page"]):p for p in load_jsonl(ROOT/"data/pages.jsonl")}
    rows,reviewed=[],[]
    for original in traces:
        t=copy.deepcopy(original)
        strategy,qid=t["strategy"],t["question_id"]
        reference="B" if strategy=="C" else strategy
        if strategy=="C" and original["hits"]!=indexed[("B",qid)]["hits"]:
            raise ValueError("C material changed; requires fresh direct review")
        for h in t["hits"]:
            meta=h["metadata"]
            page=pages[(meta["document_id"],meta["page"])]
            if page["text"][meta["char_start"]:meta["char_end"]]!=h["text"] or page["source"]!=meta["source"]:
                raise ValueError("Reviewed material differs from the saved source span")
            literal=h["evidence_hit"]
            extra=EXTRA.get((reference,qid,h["rank"]))
            if extra:
                if h["metadata"]["char_start"]!=extra[0]:
                    raise ValueError("Reviewed chunk offset changed")
                gold=t["golds"][0]
                if h["metadata"]["document_id"]!=gold["source_id"] or h["metadata"]["page"]!=gold["page"]:
                    raise ValueError("Reviewed source/page changed")
            accepted=literal or extra is not None
            reason="Một chunk đúng source/page chứa nguyên evidence đã xác minh trước chạy." if literal else (extra[1] if extra else NEGATIVE[qid])
            rows.append({"strategy":strategy,"question_id":qid,"split":t["split"],"rank":h["rank"],
                "chunk_id":h["chunk_id"],"text_sha256":hashlib.sha256(h["text"].encode()).hexdigest(),
                "source":h["metadata"]["source"],"page":h["metadata"]["page"],
                "char_start":h["metadata"]["char_start"],"char_end":h["metadata"]["char_end"],
                "literal_hit":literal,"equivalent_accepted":bool(extra and not literal),"evidence_hit":accepted,
                "requirements":REQUIREMENTS[qid],"reason":reason,"evidence_excerpt":h["text"] if accepted else None,
                "reviewer":"Codex — direct source/chunk reading, AI-assisted post-hoc review",
                "human_confirmed":False,"same_material_as":"B" if strategy=="C" else None})
            h["literal_evidence_hit"]=literal
            h["evidence_hit"]=accepted
        t["hit1"]=t["hits"][0]["evidence_hit"]
        t["hit3"]=any(h["evidence_hit"] for h in t["hits"])
        t["evaluation_version"]="reviewed-v2-posthoc-AI"
        reviewed.append(t)
    return rows,reviewed


def main():
    paths=["results/traces_dev.jsonl","results/traces_test.jsonl","benchmark/questions.jsonl"]
    traces=load_jsonl(ROOT/paths[0])+load_jsonl(ROOT/paths[1])
    rows,reviewed=build_review(traces)
    assert len(rows)==180 and len(reviewed)==60
    manifest={"version":"reviewed-v2-posthoc-AI","reviewed_at_utc":datetime.now(timezone.utc).isoformat(),
        "source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
        "method":"All distinct A/B top-3 records read directly against question requirements and source. Literal positives retained; equivalent evidence accepted only in a single source-traceable chunk. Identical C material explicitly checked, not independently rejudged.",
        "post_hoc":True,"independent_holdout":False,"human_confirmed":False,
        "selection_unchanged":"C retained from original literal dev protocol. This post-test evaluation revision does not reselect/tune retrieval.","rows":rows}
    (ROOT/"results/evidence_review_v2.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for split in ["dev","test"]:
        items=[t for t in reviewed if t["split"]==split]
        (ROOT/f"results/traces_reviewed_{split}.jsonl").write_text("".join(json.dumps(t,ensure_ascii=False)+"\n" for t in items),encoding="utf-8")
        summary=summarize(items)
        summary.update(metric="Single-chunk source/page + complete literal OR directly reviewed equivalent evidence; no multi-chunk union.",evaluation_version=manifest["version"],post_hoc=True,human_confirmed=False)
        (ROOT/f"results/metrics_reviewed_{split}.json").write_text(json.dumps(summary,indent=2)+"\n")
        print(json.dumps(summary,indent=2))
    lines=["# Evidence review v2 — đánh giá AI hỗ trợ sau thí nghiệm","",manifest["method"],"",
        "Giữ nguyên bộ câu hỏi, tham số, ranking, kết quả literal và lựa chọn C. Đây là sửa phép đánh giá sau khi đã thấy test, không phải holdout mới và chưa có con người xác nhận.",""]
    for qid in REQUIREMENTS:
        lines.extend(["## "+qid,"",REQUIREMENTS[qid],"", "| Strategy | Rank | Page/offset | Literal | Equivalent | Kết luận và lý do |", "|---|---:|---|---|---|---|"])
        for r in (r for r in rows if r["question_id"]==qid):
            lines.append(f"| {r['strategy']} | {r['rank']} | {r['page']}:{r['char_start']} | {r['literal_hit']} | {r['equivalent_accepted']} | {r['reason']} |")
        lines.append("")
    (ROOT/"results/evidence_review_v2.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
