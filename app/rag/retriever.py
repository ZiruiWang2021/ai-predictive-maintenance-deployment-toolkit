"""Retrieve maintenance manual context and generate grounded RAG answers."""

from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path
import re
from typing import Any

from app.rag.ingest import DEFAULT_INDEX_PATH, DEFAULT_MANUALS_DIR, build_index, tokenize
from app.rag.prompts import build_rag_prompt


SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")
OUT_OF_SCOPE_PATTERNS = (
    "warranty",
    "claim form",
    "password",
    "admin account",
    "hydraulic",
    "cavitation",
    "procurement",
    "lead time",
    "fire suppression",
    "building safety",
)


def load_index(index_path: Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    """Load the local vector index, creating it if missing."""
    if not index_path.exists():
        return build_index(DEFAULT_MANUALS_DIR, index_path)
    return json.loads(index_path.read_text(encoding="utf-8"))


def embed_query(question: str, idf: dict[str, float]) -> dict[str, float]:
    """Embed a question into the same sparse TF-IDF space as the index."""
    tokens = [token for token in tokenize(question) if token in idf]
    counts = Counter(tokens)
    if not counts:
        return {}
    max_count = max(counts.values())
    vector = {token: (count / max_count) * idf[token] for token, count in counts.items()}
    norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
    return {token: value / norm for token, value in vector.items()}


def cosine_sparse(left: dict[str, float], right: dict[str, float]) -> float:
    """Compute cosine similarity for normalized sparse vectors."""
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    return float(sum(value * right.get(token, 0.0) for token, value in left.items()))


def has_scope_gap(question: str) -> bool:
    """Detect topics that are outside the synthetic maintenance manual set."""
    lowered = question.lower()
    return any(pattern in lowered for pattern in OUT_OF_SCOPE_PATTERNS)


def retrieve_context(question: str, top_k: int = 4, index_path: Path = DEFAULT_INDEX_PATH) -> list[dict[str, Any]]:
    """Return the most relevant manual chunks for a question."""
    index = load_index(index_path)
    query_vector = embed_query(question, index.get("idf", {}))
    ranked: list[dict[str, Any]] = []
    for chunk in index.get("chunks", []):
        score = cosine_sparse(query_vector, chunk.get("vector", {}))
        if score <= 0:
            continue
        ranked.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "title": chunk["title"],
                "text": chunk["text"],
                "score": round(score, 4),
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[: max(1, top_k)]


def select_evidence_sentences(question: str, contexts: list[dict[str, Any]], max_sentences: int = 4) -> list[dict[str, Any]]:
    """Select compact evidence sentences from retrieved chunks."""
    question_terms = set(tokenize(question))
    evidence: list[dict[str, Any]] = []
    for context in contexts:
        sentences = SENTENCE_PATTERN.split(context["text"])
        scored_sentences: list[tuple[int, str]] = []
        for sentence in sentences:
            terms = set(tokenize(sentence))
            overlap = len(question_terms.intersection(terms))
            if overlap:
                scored_sentences.append((overlap, sentence.strip()))
        scored_sentences.sort(key=lambda item: item[0], reverse=True)
        selected = scored_sentences[0][1] if scored_sentences else context["text"][:320].strip()
        evidence.append(
            {
                "source": context["source"],
                "chunk_id": context["chunk_id"],
                "score": context["score"],
                "text": selected,
            }
        )
        if len(evidence) >= max_sentences:
            break
    return evidence


def generate_local_answer(question: str, evidence: list[dict[str, Any]]) -> str:
    """Generate a deterministic local answer from retrieved evidence."""
    if not evidence:
        return "I do not have enough retrieved maintenance evidence to answer this question."
    if has_scope_gap(question):
        return (
            "The retrieved synthetic maintenance manuals do not contain enough evidence to answer this specific "
            "question. Treat it as out of scope for the current knowledge base and verify it against the relevant "
            "OEM, procurement, IT, safety, or site procedure documents."
        )

    evidence_text = " ".join(item["text"] for item in evidence[:3])
    if "temperature" in question.lower() or "overheat" in question.lower():
        return (
            "Check whether the temperature reading is valid, then inspect cooling airflow, fan or cooling-fin blockage, "
            "load level, lubrication condition, vibration, and electrical imbalance. If the upward trend continues, "
            "reduce load where safe and schedule maintenance."
        )
    if "bearing" in question.lower():
        return (
            "Inspect vibration trend, lubrication condition, bearing temperature, alignment, and contamination. "
            "Escalate if vibration and temperature rise together or if evidence points to progressive bearing wear."
        )
    if "sensor" in question.lower() or "anomaly" in question.lower():
        return (
            "Validate the sensor reading before treating it as equipment degradation: compare with redundant signals, "
            "check calibration, inspect wiring or mounting, and look for sudden step changes or impossible values."
        )
    return (
        "Based on the retrieved maintenance notes, review the most relevant equipment symptoms, validate data quality, "
        f"and follow the documented inspection steps. Key evidence: {evidence_text[:420]}"
    )


def generate_rag_answer(question: str, top_k: int = 4, index_path: Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    """Generate a grounded RAG answer using local retrieval and a clear prompt template."""
    contexts = retrieve_context(question, top_k=top_k, index_path=index_path)
    evidence = select_evidence_sentences(question, contexts)
    source_documents = sorted({item["source"] for item in evidence})
    max_score = max((float(item["score"]) for item in evidence), default=0.0)
    scope_gap = has_scope_gap(question)
    uncertainty_note = (
        "Evidence is limited or weak; verify against the original equipment manual and maintenance history before action."
        if scope_gap or max_score < 0.12 or len(evidence) < 2
        else "Retrieved evidence is relevant for demo decision support, but it is based on synthetic demo manuals."
    )
    return {
        "question": question,
        "direct_answer": generate_local_answer(question, evidence),
        "supporting_evidence": evidence,
        "source_documents": source_documents,
        "uncertainty_note": uncertainty_note,
        "prompt_template": build_rag_prompt(question, contexts),
    }
