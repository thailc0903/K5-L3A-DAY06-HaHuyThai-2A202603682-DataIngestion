"""Review correctness: alternative evidence, incomplete evidence, changed material."""
import copy
import json
import unittest
from pathlib import Path
from scripts.review_evidence import build_review

ROOT=Path(__file__).resolve().parents[1]


class EvidenceReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traces=[json.loads(line) for split in ["dev","test"] for line in (ROOT/f"results/traces_{split}.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_alternative_same_page_instruction_accepted_in_one_chunk(self):
        rows,reviewed=build_review(self.traces)
        decision=next(r for r in rows if (r["strategy"],r["question_id"],r["rank"])==("B","q20",1))
        self.assertFalse(decision["literal_hit"])
        self.assertTrue(decision["equivalent_accepted"])
        trace=next(t for t in reviewed if (t["strategy"],t["question_id"])==("B","q20"))
        self.assertTrue(trace["hit1"])

    def test_incomplete_or_neighbor_api_evidence_stays_negative(self):
        rows,_=build_review(self.traces)
        decisions={(r["strategy"],r["question_id"],r["rank"]):r for r in rows}
        for key in [("A","q05",3),("A","q10",1),("B","q08",2),("B","q16",1)]:
            self.assertFalse(decisions[key]["evidence_hit"],key)

    def test_changed_source_text_cannot_reuse_a_prior_judgment(self):
        traces=copy.deepcopy(self.traces)
        trace=next(t for t in traces if t["strategy"]=="A" and t["question_id"]=="q02")
        trace["hits"][0]["text"]="unreviewed replacement"
        with self.assertRaisesRegex(ValueError,"source span"):
            build_review(traces)

    def test_c_is_not_implicitly_assumed_identical(self):
        traces=copy.deepcopy(self.traces)
        trace=next(t for t in traces if t["strategy"]=="C" and t["question_id"]=="q20")
        trace["hits"]=list(reversed(trace["hits"]))
        with self.assertRaisesRegex(ValueError,"C material changed"):
            build_review(traces)
