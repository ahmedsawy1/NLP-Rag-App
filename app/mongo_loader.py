"""
Load documents from MongoDB into the same in-memory store as local files (rag.documents).

Flow (high level):
  1. Connect to MongoDB using the URI from your .env file.
  2. Read each document from every collection you listed (comma-separated in .env).
  3. Turn each document into text — either the whole thing as JSON (nested / Mongoose docs)
     or only the fields you list in MONGODB_TEXT_FIELDS.
  4. Split into chunks, create embeddings — same as document_loader.py does for files.

This module uses Motor: the official *async* MongoDB driver for Python. That fits FastAPI,
which is also async-friendly.
"""

from __future__ import annotations

import json

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import (
    MONGODB_COLLECTIONS,
    MONGODB_DB,
    MONGODB_ENABLED,
    MONGODB_TEXT_FIELDS,
    MONGODB_TEXT_MODE,
    MONGODB_URI,
)
from app.rag import documents, get_embedding, split_text

# We keep one client for the whole app lifetime so we can close it cleanly on shutdown.
mongo_client: AsyncIOMotorClient | None = None


def _document_as_json_text(doc: dict) -> str:
    """
    Serialize the full document as JSON text so nested objects and arrays embed well.

    MongoDB returns special types (ObjectId, datetime, …). ``default=str`` turns them into
    plain strings so ``json.dumps`` never crashes — similar to what you see in Compass.
    """
    return json.dumps(doc, default=str, ensure_ascii=False, indent=2)


def _doc_to_text_from_fields(doc: dict) -> str:
    """
    Pick only the fields listed in MONGODB_TEXT_FIELDS and join them into one string.

    Good when you store a single ``body`` or ``text`` field and do not want ``_id`` in the chunk.
    """
    parts: list[str] = []
    for field in MONGODB_TEXT_FIELDS:
        value = doc.get(field)
        if value is None:
            continue
        # Nested dict/list: pretty JSON reads better than Python's str(list).
        if isinstance(value, (dict, list)):
            parts.append(json.dumps(value, default=str, ensure_ascii=False))
        else:
            parts.append(str(value).strip())
    return "\n\n".join(p for p in parts if p)


def _doc_to_text(doc: dict) -> str:
    """Dispatch: whole-document JSON vs selected fields (see MONGODB_TEXT_MODE in config)."""
    if MONGODB_TEXT_MODE == "json":
        return _document_as_json_text(doc)
    return _doc_to_text_from_fields(doc)


def _source_label(doc: dict, collection_name: str) -> str:
    """Short label for /documents — includes collection so you can tell categories vs products apart."""
    _id = doc.get("_id")
    return f"mongodb:{collection_name}:{_id}"


async def connect_and_load_mongodb() -> None:
    """
    Called once when the app starts (if MongoDB is enabled).

    - Opens a connection pool to MongoDB Atlas or a local server.
    - Streams documents from each configured collection and appends chunks to rag.documents.
    """
    global mongo_client

    if not MONGODB_ENABLED:
        print("ℹ️  MongoDB is disabled (set MONGODB_ENABLED=true in .env to turn it on).\n")
        return

    if not MONGODB_URI or not MONGODB_DB or not MONGODB_COLLECTIONS:
        print(
            "⚠️  MongoDB is enabled but MONGODB_URI, MONGODB_DB, or MONGODB_COLLECTION "
            "(comma-separated list) is missing. Check your .env file.\n"
        )
        return

    # In "fields" mode we need at least one field name; "json" mode uses the whole document.
    if MONGODB_TEXT_MODE == "fields" and not MONGODB_TEXT_FIELDS:
        print(
            "⚠️  MONGODB_TEXT_MODE is 'fields' but MONGODB_TEXT_FIELDS is empty. "
            "Add field names, or set MONGODB_TEXT_MODE=json for nested / JSON documents.\n"
        )
        return

    try:
        # AsyncIOMotorClient talks to MongoDB without blocking the whole server on I/O.
        mongo_client = AsyncIOMotorClient(MONGODB_URI)
        db = mongo_client[MONGODB_DB]

        mode_hint = "whole document as JSON" if MONGODB_TEXT_MODE == "json" else f"fields: {', '.join(MONGODB_TEXT_FIELDS)}"
        coll_list = ", ".join(MONGODB_COLLECTIONS)
        print(f"🍃 Loading from MongoDB: {MONGODB_DB} → [{coll_list}] ({mode_hint}) ...\n")

        total_docs_all = 0
        total_chunks_all = 0

        for coll_name in MONGODB_COLLECTIONS:
            collection = db[coll_name]
            print(f"   📂 Collection “{coll_name}”")

            # Quick sanity check: empty collection looks the same as a wrong collection name.
            total_in_coll = await collection.count_documents({})
            print(f"      📊 Documents: {total_in_coll}")
            if total_in_coll == 0:
                try:
                    # Same cluster your URI points at — helps when MONGODB_DB is wrong (very common).
                    _system = frozenset({"admin", "local", "config"})
                    db_names = sorted(await mongo_client.list_database_names())
                    user_dbs = [n for n in db_names if n not in _system]

                    all_coll = sorted(await db.list_collection_names())
                    coll_preview = ", ".join(all_coll[:25]) if all_coll else "(none — this database has no collections yet)"
                    if len(all_coll) > 25:
                        coll_preview += f", … (+{len(all_coll) - 25} more)"

                    print(
                        "      ℹ️  This collection is empty. Check the name in Compass matches "
                        f"“{coll_name}”, and that MONGODB_DB is the database (not the cluster name).\n"
                    )
                    print(f"      ℹ️  Collections under database “{MONGODB_DB}”: {coll_preview}")
                    db_preview = ", ".join(user_dbs[:30]) if user_dbs else "(none listed)"
                    if len(user_dbs) > 30:
                        db_preview += f", … (+{len(user_dbs) - 30} more)"
                    print(
                        f"      ℹ️  Non-system databases on this cluster: {db_preview}\n"
                        "      ℹ️  Use MONGODB_COLLECTION=name1,name2 for multiple collections.\n"
                    )
                except Exception as list_err:
                    print(f"      ℹ️  (Could not list databases/collections: {list_err})\n")

            count = 0
            chunk_total = 0

            # find({}) means "all documents" — good for learning; later you can add a filter.
            async for doc in collection.find({}):
                text = _doc_to_text(doc)
                if not text.strip():
                    why = "empty after JSON serialization" if MONGODB_TEXT_MODE == "json" else "no text in configured fields"
                    print(f"      ⚠️  Skipping document {doc.get('_id')!r}: {why}.")
                    continue

                source = _source_label(doc, coll_name)
                chunks = split_text(text)
                for chunk in chunks:
                    chunk = chunk.strip()
                    if not chunk:
                        continue
                    # get_embedding uses OpenAI and is synchronous — fine for a small demo.
                    embedding = get_embedding(chunk)
                    documents.append({
                        "text": chunk,
                        "embedding": embedding,
                        "source": source,
                    })
                    chunk_total += 1

                count += 1

            total_docs_all += count
            total_chunks_all += chunk_total
            print(f"      ✅ {count} document(s) → {chunk_total} chunk(s).\n")

        print(f"   ✅ MongoDB total: {total_docs_all} document(s) → {total_chunks_all} chunk(s).\n")
    except Exception as e:
        # Beginners: seeing the real error helps you fix URI, IP allowlist, or password issues.
        print(f"⚠️  Could not load from MongoDB: {e}\n")


def disconnect_mongodb() -> None:
    """
    Called when the app shuts down.

    Closing the client frees network resources and is considered good practice.
    (Motor's close() is synchronous — we still call it from the async lifespan.)
    """
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None
