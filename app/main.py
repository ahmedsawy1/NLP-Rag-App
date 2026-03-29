"""
App entry point — creates the FastAPI app and wires everything together.

Uses the modern 'lifespan' approach (instead of the deprecated on_event).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.document_loader import load_documents
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup (before yield) and shutdown (after yield)."""
    load_documents()
    yield


app = FastAPI(title="Beginner RAG App", lifespan=lifespan)
app.include_router(router)
