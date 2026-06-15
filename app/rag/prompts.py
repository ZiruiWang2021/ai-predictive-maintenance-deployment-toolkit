"""Prompt templates for the maintenance RAG assistant."""

from __future__ import annotations

from collections.abc import Sequence


RAG_SYSTEM_PROMPT = """You are a maintenance engineering assistant.
Use only the retrieved maintenance context to answer the question.
If the evidence is incomplete, say what is missing and avoid pretending certainty.
Return a concise answer with supporting evidence and source document names."""


RAG_ANSWER_TEMPLATE = """System:
{system_prompt}

Question:
{question}

Retrieved context:
{context}

Answer format:
1. Direct answer
2. Supporting evidence
3. Source document names
4. Uncertainty note if evidence is insufficient
"""


def format_context_blocks(contexts: Sequence[dict[str, object]]) -> str:
    """Format retrieved chunks for prompt injection."""
    if not contexts:
        return "No relevant context retrieved."

    blocks: list[str] = []
    for index, item in enumerate(contexts, start=1):
        source = item.get("source", "unknown")
        chunk_id = item.get("chunk_id", f"chunk-{index}")
        text = str(item.get("text", "")).strip()
        blocks.append(f"[{index}] source={source} chunk={chunk_id}\n{text}")
    return "\n\n".join(blocks)


def build_rag_prompt(question: str, contexts: Sequence[dict[str, object]]) -> str:
    """Create the final RAG prompt for an LLM or local answer generator."""
    return RAG_ANSWER_TEMPLATE.format(
        system_prompt=RAG_SYSTEM_PROMPT,
        question=question.strip(),
        context=format_context_blocks(contexts),
    )
