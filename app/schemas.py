"""
Pydantic models — define the shape of request/response data.
"""

from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Source(BaseModel):
    text: str
    source: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class DocumentsResponse(BaseModel):
    total_chunks: int
    sources: list[str]
