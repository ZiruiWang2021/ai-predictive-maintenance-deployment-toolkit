"""Build a lightweight local vector index from maintenance manual documents."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANUALS_DIR = PROJECT_ROOT / "data" / "manuals"
DEFAULT_INDEX_PATH = PROJECT_ROOT / "data" / "rag_index" / "manual_index.json"

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")
SUPPORTED_EXTENSIONS = {".md", ".txt"}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True)
class ManualChunk:
    """A chunk of a maintenance manual."""

    chunk_id: str
    source: str
    title: str
    text: str
    token_count: int


def tokenize(text: str) -> list[str]:
    """Tokenize text for the local sparse embedding backend."""
    return [token for token in TOKEN_PATTERN.findall(text.lower()) if token not in STOPWORDS and len(token) > 1]


def iter_manual_files(manuals_dir: Path) -> Iterable[Path]:
    """Yield supported manual files in deterministic order."""
    if not manuals_dir.exists():
        return []
    return sorted(path for path in manuals_dir.rglob("*") if path.suffix.lower() in SUPPORTED_EXTENSIONS)


def read_title(text: str, fallback: str) -> str:
    """Read the first markdown heading as a title."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def chunk_text(text: str, source: str, max_tokens: int = 180, overlap: int = 40) -> list[ManualChunk]:
    """Split a document into overlapping token windows while preserving readable text."""
    words = text.split()
    if not words:
        return []

    title = read_title(text, fallback=source)
    chunks: list[ManualChunk] = []
    start = 0
    chunk_number = 1
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk_words = words[start:end]
        chunk_id = f"{Path(source).stem}-{chunk_number:03d}"
        chunks.append(
            ManualChunk(
                chunk_id=chunk_id,
                source=source,
                title=title,
                text=" ".join(chunk_words),
                token_count=len(tokenize(" ".join(chunk_words))),
            )
        )
        if end == len(words):
            break
        start = max(0, end - overlap)
        chunk_number += 1
    return chunks


def ensure_sample_manual(manuals_dir: Path) -> Path:
    """Create a small synthetic demo manual when no manuals exist."""
    manuals_dir.mkdir(parents=True, exist_ok=True)
    sample_path = manuals_dir / "sample_motor_temperature_guide.md"
    if sample_path.exists():
        return sample_path
    sample_path.write_text(
        """# Sample Motor Temperature Guide

Synthetic demo document for portfolio use only. It is not a real OEM manual.

When motor temperature rises abnormally, first confirm that the temperature sensor is calibrated and mounted correctly. Compare the reading with a secondary thermometer if available. Then check cooling airflow, fan condition, dust blockage, lubrication condition, load level, and recent operating changes.

High temperature combined with vibration may indicate bearing wear, shaft misalignment, or lubrication breakdown. High temperature without vibration may point to blocked cooling paths, overload, excessive ambient temperature, or electrical imbalance.

Recommended action: reduce load if safe, inspect airflow and cooling fins, verify lubrication, check current imbalance across phases, and schedule maintenance if the temperature trend continues upward.
""",
        encoding="utf-8",
    )
    return sample_path


def collect_chunks(manuals_dir: Path) -> list[ManualChunk]:
    """Load manuals and return all chunks."""
    manuals_dir.mkdir(parents=True, exist_ok=True)
    manual_files = list(iter_manual_files(manuals_dir))
    if not manual_files:
        ensure_sample_manual(manuals_dir)
        manual_files = list(iter_manual_files(manuals_dir))

    chunks: list[ManualChunk] = []
    for path in manual_files:
        text = path.read_text(encoding="utf-8")
        chunks.extend(chunk_text(text, source=path.name))
    return chunks


def build_sparse_vectors(chunks: list[ManualChunk]) -> tuple[dict[str, float], list[dict[str, float]]]:
    """Build normalized TF-IDF sparse vectors for each chunk."""
    tokenized_chunks = [tokenize(chunk.text) for chunk in chunks]
    doc_frequency: Counter[str] = Counter()
    for tokens in tokenized_chunks:
        doc_frequency.update(set(tokens))

    total_docs = max(len(chunks), 1)
    idf = {
        token: math.log((1 + total_docs) / (1 + count)) + 1.0
        for token, count in sorted(doc_frequency.items())
    }

    vectors: list[dict[str, float]] = []
    for tokens in tokenized_chunks:
        counts = Counter(tokens)
        if not counts:
            vectors.append({})
            continue
        max_count = max(counts.values())
        vector = {token: (count / max_count) * idf[token] for token, count in counts.items()}
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        vectors.append({token: value / norm for token, value in vector.items()})
    return idf, vectors


def build_index(manuals_dir: Path = DEFAULT_MANUALS_DIR, index_path: Path = DEFAULT_INDEX_PATH) -> dict[str, object]:
    """Build and persist the local vector index."""
    chunks = collect_chunks(manuals_dir)
    idf, vectors = build_sparse_vectors(chunks)
    try:
        manuals_dir_display = str(manuals_dir.relative_to(PROJECT_ROOT))
    except ValueError:
        manuals_dir_display = str(manuals_dir)

    index = {
        "version": 1,
        "embedding_backend": "local_tfidf_sparse",
        "manuals_dir": manuals_dir_display,
        "chunk_count": len(chunks),
        "chunks": [
            {
                **asdict(chunk),
                "vector": vector,
            }
            for chunk, vector in zip(chunks, vectors)
        ],
        "idf": idf,
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest maintenance manuals into a local RAG vector index.")
    parser.add_argument("--manuals-dir", default=str(DEFAULT_MANUALS_DIR), help="Directory containing .md/.txt manuals.")
    parser.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH), help="Output JSON index path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    index = build_index(Path(args.manuals_dir), Path(args.index_path))
    print(f"Wrote {args.index_path}")
    print(f"Indexed {index['chunk_count']} chunks from {args.manuals_dir}")


if __name__ == "__main__":
    main()
