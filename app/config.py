"""
Configuration — loads env vars and creates the OpenAI client.

Everything else imports from here so there's a single source of truth.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

DATA_DIR = Path(__file__).parent.parent / "data"

client = OpenAI(api_key=OPENAI_API_KEY)


def _env_bool(name: str, default: bool = False) -> bool:
    """Read true/false from env (beginner-friendly: accepts 'true', '1', 'yes')."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


# ── MongoDB (optional) ─────────────────────────────────────────────────
# Set these in your .env file. If MONGODB_ENABLED is false, the app ignores Mongo.
MONGODB_ENABLED = _env_bool("MONGODB_ENABLED", default=False)
MONGODB_URI = os.getenv("MONGODB_URI")  # e.g. mongodb+srv://user:pass@cluster/...
MONGODB_DB = os.getenv("MONGODB_DB", "")

# One collection name, or several separated by commas (e.g. categories,products,sessions).
_raw_coll = os.getenv("MONGODB_COLLECTION", "")
MONGODB_COLLECTIONS = [c.strip() for c in _raw_coll.split(",") if c.strip()]

# How each MongoDB document becomes text for chunking + embeddings:
#   "json"   — serialize the whole document as JSON (best for nested / Mongoose-style docs).
#   "fields" — only concatenate the field names in MONGODB_TEXT_FIELDS (e.g. title,body).
MONGODB_TEXT_MODE = os.getenv("MONGODB_TEXT_MODE", "json").strip().lower()
if MONGODB_TEXT_MODE not in ("json", "fields"):
    MONGODB_TEXT_MODE = "json"

# Comma-separated field names when MONGODB_TEXT_MODE=fields (ignored in json mode).
_raw_fields = os.getenv("MONGODB_TEXT_FIELDS", "text")
MONGODB_TEXT_FIELDS = [f.strip() for f in _raw_fields.split(",") if f.strip()]
