"""
Document loader — reads .txt files from the data/ folder on startup.

Splits each file into chunks, creates embeddings, and stores them
in the in-memory vector store (rag.documents).
"""

from app.config import DATA_DIR
from app.rag import documents, get_embedding, split_text


def load_documents():
    """Read all .txt files in data/, split into chunks, and create embeddings."""
    if not DATA_DIR.exists():
        print(f"⚠️  Data folder not found: {DATA_DIR}")
        return

    txt_files = list(DATA_DIR.glob("*.txt"))
    if not txt_files:
        print("⚠️  No .txt files found in data/ folder")
        return

    print(f"📂 Loading {len(txt_files)} file(s) from {DATA_DIR} ...")

    for file_path in txt_files:
        text = file_path.read_text(encoding="utf-8")
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
