"""
RAG core logic — chunking, embeddings, and vector search.

This is where the "Retrieval" part of RAG happens:
  1. split_text()           → break documents into small pieces
  2. get_embedding()        → turn text into a vector of numbers
  3. cosine_similarity()    → measure how similar two vectors are
  4. find_relevant_chunks() → find the best matching chunks for a question
"""

import numpy as np

from app.config import EMBEDDING_MODEL, client

# ── In-memory vector store ────────────────────────────────────────────
# Each item: {"text": "...", "embedding": [...], "source": "file.txt"}
documents: list[dict] = []


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks so we don't lose context at boundaries."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embedding(text: str) -> list[float]:
    """Turn text into a vector (list of numbers) using OpenAI's embedding model."""
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Measure how similar two vectors are. Returns a number between -1 and 1."""
    a_arr, b_arr = np.array(a), np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


def find_relevant_chunks(question: str, top_k: int = 3) -> list[tuple[float, str, str]]:
    """Find the most relevant document chunks for a given question."""
    question_embedding = get_embedding(question)

    scored = []
    for doc in documents:
        score = cosine_similarity(question_embedding, doc["embedding"])
        scored.append((score, doc["text"], doc["source"]))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
