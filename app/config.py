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
