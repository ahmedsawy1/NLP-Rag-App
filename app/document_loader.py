"""
Document loader — reads .txt and .pdf files from the data/ folder on startup.

Splits each file into chunks, creates embeddings, and stores them
in the in-memory vector store (rag.documents).
"""

from pathlib import Path

from pypdf import PdfReader

from app.config import DATA_DIR
from app.rag import documents, get_embedding, split_text


def _read_pdf(path: Path) -> str:
    reader = PdfReader(path)
    parts: list[str] = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    return "\n\n".join(parts)


def _read_file_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        return _read_pdf(file_path)
    return file_path.read_text(encoding="utf-8")


def load_documents():
    """Read all .txt and .pdf files in data/, split into chunks, and create embeddings."""
    if not DATA_DIR.exists():
        print(f"⚠️  Data folder not found: {DATA_DIR}")
        return

    paths = sorted(DATA_DIR.glob("*.txt")) + sorted(DATA_DIR.glob("*.pdf"))
    if not paths:
        print("⚠️  No .txt or .pdf files found in data/ folder")
        return

    print(f"📂 Loading {len(paths)} file(s) from {DATA_DIR} ...")

    for file_path in paths:
        text = _read_file_text(file_path)
        if not text.strip():
            print(f"   ⚠️  {file_path.name}: no text extracted, skipped")
            continue
        chunks = split_text(text)

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            embedding = get_embedding(chunk)
            documents.append({
                "text": chunk,
                "embedding": embedding,
                "source": file_path.name,
            })

        print(f"   ✅ {file_path.name} → {len(chunks)} chunks")

    print(f"✅ Done! {len(documents)} total chunks loaded.\n")
