"""RAG module smoke tests."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.ingest import build_index
from app.rag.retriever import generate_rag_answer, retrieve_context


class RagTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="pdm_rag_test_"))
        self.manuals_dir = self.temp_dir / "manuals"
        self.index_path = self.temp_dir / "index.json"
        self.manuals_dir.mkdir(parents=True)
        (self.manuals_dir / "motor_overheating_guide.md").write_text(
            """# Motor Overheating Guide

Synthetic demo manual. If motor temperature rises abnormally, first validate the temperature sensor,
then inspect cooling airflow, fan condition, blocked ventilation, load level, lubrication, and current imbalance.
High temperature with vibration can indicate bearing wear or shaft misalignment.
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_build_index_creates_chunks(self) -> None:
        index = build_index(self.manuals_dir, self.index_path)
        self.assertTrue(self.index_path.exists())
        self.assertGreater(index["chunk_count"], 0)
        self.assertEqual(index["embedding_backend"], "local_tfidf_sparse")

    def test_retrieve_context_returns_relevant_manual(self) -> None:
        build_index(self.manuals_dir, self.index_path)
        contexts = retrieve_context("What should I check if motor temperature rises?", index_path=self.index_path)
        self.assertGreater(len(contexts), 0)
        self.assertEqual(contexts[0]["source"], "motor_overheating_guide.md")

    def test_generate_rag_answer_has_required_fields(self) -> None:
        build_index(self.manuals_dir, self.index_path)
        answer = generate_rag_answer("What should I check if the motor temperature rises?", index_path=self.index_path)
        self.assertIn("direct_answer", answer)
        self.assertIn("supporting_evidence", answer)
        self.assertIn("source_documents", answer)
        self.assertIn("uncertainty_note", answer)
        self.assertIn("motor_overheating_guide.md", answer["source_documents"])


if __name__ == "__main__":
    unittest.main()
