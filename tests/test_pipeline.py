"""Focused correctness checks for metrics, source offsets and persistence."""
import tempfile
import unittest
from starter.src.models import DocumentPage
from starter.src.ingestion import normalize_text
from starter.src.chunking import fixed_size, by_paragraph
from starter.src.evaluation import evaluate_query, summarize
from starter.src.store import QdrantStore


class PipelineTests(unittest.TestCase):
    def page(self):
        return DocumentPage("doc", "https://example.invalid/doc", "unit", "# Heading\n\n" + "One complete sentence. " * 70 + "\n\nSecond paragraph.", {"category": "text"})

    def test_source_spans_and_determinism(self):
        page = self.page()
        for chunks in [fixed_size(page, 100, 10), by_paragraph(page, 180)]:
            covered = set()
            for c in chunks:
                start, end = c.metadata["char_start"], c.metadata["char_end"]
                self.assertEqual(page.text[start:end], c.text)
                self.assertEqual(c.metadata["category"], "text")
                self.assertLessEqual(len(c.text), 180)
                covered.update(range(start,end))
            self.assertTrue(all(i in covered for i,ch in enumerate(page.text) if not ch.isspace()))
        self.assertEqual(fixed_size(page, 100, 10), fixed_size(page, 100, 10))
        with self.assertRaises(ValueError):
            fixed_size(page, 100, 100)

    def test_normalization(self):
        self.assertEqual(normalize_text("e\u0301\u00a0 x\r\n\r\n\r\nY"), "é x\n\nY")

    def test_evidence_is_not_source_only_or_multichunk(self):
        q = {"id": "q", "split": "dev", "question": "?", "expected_answer": "both", "gold_source_id": "doc", "gold_page": "unit", "evidence_quote": "alpha beta"}
        def hit(text, document_id="doc"):
            return {"chunk_id": text, "text": text, "score": 1.0, "metadata": {"document_id": document_id, "page": "unit"}}
        trace = evaluate_query(q, [hit("alpha"), hit("beta"), hit("alpha beta", "wrong")])
        self.assertFalse(trace["hit1"])
        self.assertFalse(trace["hit3"])
        trace = evaluate_query(q, [hit("alpha"), hit("alpha beta")])
        self.assertFalse(trace["hit1"])
        self.assertTrue(trace["hit3"])
        q["alternative_gold"] = [{"source_id": "alt", "page": "unit", "evidence_quote": "equivalent"}]
        self.assertTrue(evaluate_query(q, [hit("equivalent", "alt")])["hit1"])
        trace.update(strategy="A")
        self.assertIsNone(summarize([trace])["rows"][0]["filter_compliance"])

    def test_qdrant_reload_filter_stale_removal_and_reopen(self):
        with tempfile.TemporaryDirectory() as path:
            store = QdrantStore(path, 3)
            store.create_schema()
            chunks = fixed_size(self.page(), 100, 0)[:2]
            chunks[1].metadata["category"] = "binary"
            vectors = [[1.,0.,0.], [0.9,0.1,0.]]
            store.upsert("A", chunks, vectors)
            store.upsert("A", chunks, vectors)
            self.assertEqual(store.count("A"), 2)
            self.assertEqual(store.search("A", vectors[0], filters={"category": "binary"})[0]["metadata"]["category"], "binary")
            with self.assertRaises(ValueError):
                store.search("A", vectors[0], filters={"document_id": "doc"})
            with self.assertRaises(ValueError):
                store.search("A", [1.,0.])
            store.upsert("A", chunks[:1], vectors[:1])
            self.assertEqual(store.count("A"), 1)
            store.close()
            reopened = QdrantStore(path, 3)
            self.assertEqual(reopened.count("A"), 1)
            self.assertEqual(reopened.search("A", vectors[0])[0]["chunk_id"], chunks[0].chunk_id)
            reopened.close()

if __name__ == "__main__":
    unittest.main()
