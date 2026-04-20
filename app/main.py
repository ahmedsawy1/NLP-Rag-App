"""
App entry point — creates the FastAPI app and wires everything together.

Uses the modern 'lifespan' approach (instead of the deprecated on_event).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.document_loader import load_documents
from app.mongo_loader import connect_and_load_mongodb, disconnect_mongodb
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: load local files from data/, then optionally pull text from MongoDB.

    Shutdown: close the MongoDB connection pool if we opened one.
    """
    # Read .txt / .pdf from the data/ folder.
    load_documents()

    # If MONGODB_ENABLED=true in .env, embed documents from your collection too.
    await connect_and_load_mongodb()

    yield

    # Tidy up network resources when Uvicorn stops.
    disconnect_mongodb()


app = FastAPI(title="Beginner RAG App", lifespan=lifespan)
app.include_router(router)
