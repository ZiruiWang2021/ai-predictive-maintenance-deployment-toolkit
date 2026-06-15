"""FastAPI backend for the predictive maintenance toolkit."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agent.schemas import AgentRunRequest, AgentRunResponse
from app.agent.workflow import run_agent
from app.rag.retriever import generate_rag_answer


class RagQueryRequest(BaseModel):
    """Request body for RAG maintenance questions."""

    question: str = Field(..., min_length=3, description="Maintenance question to answer from the manual knowledge base.")
    top_k: int = Field(4, ge=1, le=8, description="Maximum number of manual chunks to retrieve.")


class EvidenceItem(BaseModel):
    """Evidence sentence returned by the retriever."""

    source: str
    chunk_id: str
    score: float
    text: str


class RagQueryResponse(BaseModel):
    """Structured RAG response."""

    question: str
    direct_answer: str
    supporting_evidence: list[EvidenceItem]
    source_documents: list[str]
    uncertainty_note: str
    prompt_template: str


app = FastAPI(
    title="AI Predictive Maintenance Toolkit API",
    description="FastAPI backend for RUL prediction, maintenance manual RAG, and agent workflows.",
    version="0.2.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok"}


@app.post("/rag/query", response_model=RagQueryResponse)
def rag_query(request: RagQueryRequest) -> dict[str, Any]:
    """Answer a maintenance question using the local RAG knowledge base."""
    return generate_rag_answer(request.question, top_k=request.top_k)


@app.post("/agent/run", response_model=AgentRunResponse)
def agent_run(request: AgentRunRequest) -> AgentRunResponse:
    """Run the ReACT-style predictive maintenance diagnosis agent."""
    return run_agent(request)
