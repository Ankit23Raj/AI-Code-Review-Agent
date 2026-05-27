import unittest
from unittest.mock import patch

from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown
from app.reviewer.schemas import Finding
from app.reviewer.review_pipeline import review_payload
from app.workers import review_worker


SAMPLE_PAYLOAD = {
    "repo_path": "AI-Code-Review-Agent",
    "pr_number": 1,
    "changed_files": [
        {
            "file_path": "app/main.py",
            "content": "print('hello')",
        }
    ],
}


class IntegrationStagesTest(unittest.TestCase):
    def test_stage_1_payload_generation(self):
        result = review_payload(SAMPLE_PAYLOAD)
        self.assertIn("Found", result["summary"])
        self.assertIn("markdown", result)

    def test_stage_2_payload_to_pipeline(self):
        result = review_payload(SAMPLE_PAYLOAD)
        self.assertIn("markdown", result)

    def test_stage_3_aggregation(self):
        aggregated = aggregate_findings([
            Finding(
                severity="HIGH",
                category="AI Security Review",
                file_path="app/main.py",
                line_start=1,
                line_end=1,
                message="Issue",
                suggestion="Fix it",
                confidence=1.0,
                agent_name="security",
            ),
        ])
        self.assertEqual(len(aggregated.findings), 1)

    def test_stage_4_markdown_formatter(self):
        markdown = format_review_markdown({
            "summary": "AI Review Summary",
            "findings": [
                {
                    "category": "AI Security Review",
                    "message": "Issue",
                    "file_path": "app/main.py",
                    "suggestion": "Fix it",
                    "agent_name": "security",
                }
            ],
            "files_reviewed": 1,
        })
        self.assertIn("AI Review Summary", markdown)

    def test_stage_5_full_worker_flow_mocked(self):
        with patch.object(review_worker, "post_pr_comment", return_value=True), \
            patch.object(review_worker, "append_review_history", return_value=None):
            result = review_worker.process_review(SAMPLE_PAYLOAD)

        self.assertIn("review_text", result)
        self.assertIn("findings", result)


if __name__ == "__main__":
    unittest.main()