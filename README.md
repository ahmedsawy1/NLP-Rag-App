# RAG Application

A Retrieval-Augmented Generation (RAG) application built with FastAPI for intelligent document search and question answering.

## Features

- FastAPI-based REST API for RAG operations
- Document retrieval and augmented generation
- Scalable architecture with async support

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set up environment variables:
```bash
cp .env.example .env
```

2. Edit `.env` file with your configuration settings (API keys, database connections, etc.)

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
rag-app/
├── assets/              # Static assets and resources
├── LICENSE              # Apache License 2.0
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Dependencies

- `fastapi==0.115.5` - Modern, fast web framework for building APIs
- `uvicorn==0.32.0` - ASGI server for running FastAPI applications
- `python-multipart==0.0.20` - Support for multipart form data

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
