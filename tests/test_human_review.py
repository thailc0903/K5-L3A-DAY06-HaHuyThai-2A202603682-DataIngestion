"""Human-review requirements must never be auto-confirmed from AI suggestions."""
import unittest
from scripts.human_review import assess


class HumanReviewTests(unittest.TestCase):
    def template(self):
        return {"review_id":"coherence|A|example|1","kind":"coherence","strategy":"A","sample":"example","rank":"","chunk_ids":"unit-test-material","suggested_score":2}

    def test_ai_suggestion_does_not_count_as_student_review(self):
        expected=self.template()
        status,complete=assess([dict(expected)],[expected])
        self.assertEqual(status["completed_records"],0)
        self.assertFalse(status["all_complete"])
        self.assertEqual(complete,[])

    def test_confirmation_without_score_reason_and_identity_is_invalid(self):
        expected=self.template()
        row={**expected,"student_confirmed":"yes"}
        status,_=assess([row],[expected])
        self.assertFalse(status["all_complete"])
        self.assertEqual(status["invalid_rows"],[expected["review_id"]])
