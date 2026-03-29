# Beginner RAG App

A simple **Retrieval-Augmented Generation** app built with FastAPI and OpenAI.

Put `.txt` files in the `data/` folder — the app loads them on startup. Then ask questions via the API.

## How RAG Works

```
1. Startup: read all .txt files in data/   →  split into small chunks
2. Each chunk                              →  turned into an embedding (vector of numbers)
3. POST /ask with a question               →  find the most similar chunks (cosine similarity)
4. Send chunks + question to GPT           →  get an answer grounded in your docs
```

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Add your OpenAI API key to .env
#    (create a .env file with: OPENAI_API_KEY=sk-...)

# 3. Put your .txt files in the data/ folder

# 4. Run the app
uv run uvicorn app.main:app --reload

# 5. Use Postman to call the API at http://localhost:8000
```

## API Endpoints

### `POST /ask` — Ask a question

```json
{
  "question": "How do you define a function in Python?"
}
```

### `GET /documents` — See loaded documents

Returns the number of chunks and source file names.

## Project Structure

```
├── app/
│   ├── main.py              # App creation + lifespan (entry point)
│   ├── config.py            # Settings, env vars, OpenAI client
│   ├── schemas.py           # Pydantic request/response models
│   ├── rag.py               # Chunking, embeddings, vector search
│   ├── document_loader.py   # Loads .txt files from data/ on startup
│   └── routes.py            # API endpoints (/ask, /documents)
├── data/
│   └── *.txt                # Your documents go here
├── .env                     # Your API key (not committed to git)
└── pyproject.toml           # Dependencies managed by uv
```
