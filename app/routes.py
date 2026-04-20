"""
API routes — the endpoints you call from Postman.

  POST /ask        → ask a question about your documents
  GET  /documents  → see what's currently loaded
"""

from fastapi import APIRouter

from app.config import CHAT_MODEL, client
from app.prompts import load_prompt
from app.rag import documents, find_relevant_chunks
from app.schemas import AskResponse, DocumentsResponse, Question, Source

router = APIRouter()

RAG_SYSTEM_PROMPT = load_prompt("system_rag.txt")


@router.post("/ask", response_model=AskResponse)
def ask_question(body: Question):
    """Ask a question → find relevant chunks → get AI answer."""
    if not documents:
        return AskResponse(
            answer=(
                "No documents loaded. Add .txt or .pdf files under data/, "
                "and/or enable MongoDB in .env (MONGODB_ENABLED=true with a valid URI), then restart."
            ),
            sources=[],
        )

    relevant = find_relevant_chunks(body.question)

    context = "\n\n---\n\n".join(
        f"[From: {source}]\n{text}" for score, text, source in relevant
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {body.question}",
            },
        ],
    )

    return AskResponse(
        answer=response.choices[0].message.content,
        sources=[
            Source(text=text[:200], source=source, score=round(score, 3))
            for score, text, source in relevant
        ],
    )


@router.get("/documents", response_model=DocumentsResponse)
def list_documents():
    """See what documents are currently loaded."""
    sources = list(set(doc["source"] for doc in documents))
    return DocumentsResponse(total_chunks=len(documents), sources=sources)
