# webdata-api-coursework

Data-driven RESTful API built with FastAPI, SQLite and Swagger for XJCO3011 coursework.

🚀 **Live Deployment**: [https://webdata-api-coursework.onrender.com](https://webdata-api-coursework.onrender.com)
📄 **Static API Documentation (PDF)**: [docs/API.pdf](./docs/API.pdf)

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- Swagger (OpenAPI) auto docs
- Pytest + HTTPX (testing)

## Project Structure

```text
app/
  api/
    routes/
  core/
  crud/
  db/
  models/
  schemas/
data/
scripts/
tests/
docs/
archive/
render.yaml
mcp_server.py
```

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies.
3. (Optional, first run) Seed SQLite from cleaned CSV files.
4. Run API server.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
py -3 -m scripts.seed_sqlite
uvicorn app.main:app --reload
```

App startup creates database tables automatically, but it does not import CSV data automatically.

## Environment Variables

- `DATABASE_URL`: database connection string. Default: `sqlite:///./app.db`
- `API_KEY`: API key for write operations. Local default: `xjco3011-secret-key`; production should override via environment variables (do not commit production secrets).

Example:

```bash
# PowerShell
$env:DATABASE_URL="sqlite:///./app.db"
$env:API_KEY="your-secret-key"
```

## API Docs

**Live Online Documentation:**
- Swagger UI (Interactive): [https://webdata-api-coursework.onrender.com/docs](https://webdata-api-coursework.onrender.com/docs)
- ReDoc (Detailed): [https://webdata-api-coursework.onrender.com/redoc](https://webdata-api-coursework.onrender.com/redoc)

**Local Development Documentation (When running `uvicorn`):**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication

The following write endpoints require header `X-API-Key: <your_api_key>`:

- `POST /api/books`
- `PUT /api/books/{book_id}`
- `DELETE /api/books/{book_id}`
- `POST /api/books/{book_id}/reviews`

## Current Endpoints

- `GET /api/health`
- `GET /api/books`
- `GET /api/books/stats`
- `GET /api/books/{book_id}`
- `POST /api/books` (requires `X-API-Key`)
- `PUT /api/books/{book_id}` (requires `X-API-Key`)
- `DELETE /api/books/{book_id}` (requires `X-API-Key`)
- `GET /api/books/{book_id}/reviews`
- `POST /api/books/{book_id}/reviews` (requires `X-API-Key`)

## Testing

Run tests with:

```bash
pytest -q
```

Or use verbose output:

```bash
pytest -v
```

## Data Notes

- Raw source files are stored under `archive/` (ignored by git due to size).
- Processed files used by the app are stored under `data/`.
