"""Prompt text files live next to this package (see *.txt in this folder)."""

from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(name: str) -> str:
    """Load a UTF-8 prompt file from app/prompts/."""
    path = _PROMPTS_DIR / name
    return path.read_text(encoding="utf-8").strip()
