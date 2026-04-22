# FastAPI + uv — production-style image (PORT from env for cloud hosts)
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY app ./app
COPY data ./data

EXPOSE 8000

# Cloud platforms set PORT; default 8000 for local docker run -p 8000:8000
CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
