# webdata-api-coursework

Data-driven RESTful API built with FastAPI, SQLite and Swagger for XJCO3011 coursework.

🚀 **Live Deployment**: [https://cw1-books-api.onrender.com](https://cw1-books-api.onrender.com)
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

| Variable | Purpose | Local default |
|----------|---------|----------------|
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./app.db` |
| `API_KEY` | Required for write endpoints (header `X-API-Key`) | `xjco3011-secret-key` (see `app/core/config.py`) |

**Local example (PowerShell):**

```powershell
$env:DATABASE_URL = "sqlite:///./app.db"
$env:API_KEY = "your-secret-key"
```

**Production (Render)**  
Service name in [`render.yaml`](./render.yaml): `cw1-books-api`. Set secrets in the Render dashboard: **Dashboard → your web service → Environment**:

- **`API_KEY`**: use a strong random value. The app reads this at runtime; do not commit real production keys to git. If you use the same value as local development for coursework, set it explicitly here so it matches what you use in clients/tests.
- **`DATABASE_URL`**: optional; if unset, the default SQLite path applies (ephemeral disk on Render resets on redeploy unless you use a persistent disk or external DB).

You can also define these in `render.yaml` under `envVars` for non-secret defaults, but prefer the dashboard or Render **Secret** files for real API keys.

## API Docs

**Live Online Documentation:**
- Swagger UI (Interactive): [https://cw1-books-api.onrender.com/docs](https://cw1-books-api.onrender.com/docs)
- ReDoc (Detailed): [https://cw1-books-api.onrender.com/redoc](https://cw1-books-api.onrender.com/redoc)

**Local Development Documentation (When running `uvicorn`):**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication

The following write endpoints require header `X-API-Key: <your_api_key>`. The value must match `API_KEY` for that environment (local env or Render **Environment**; see above).

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

Automated tests use **in-memory SQLite** (see `tests/conftest.py`). `tests/test_books.py` covers books list/pagination/filters, stats, CRUD, `X-API-Key` (403), validation (422), and 404. `tests/test_reviews.py` covers listing/creating reviews (including `min_score` and pagination). `tests/test_health.py` covers `GET /api/health`.

```bash
pytest -q
pytest -v
```

To fail the run if any warning appears (stricter CI-style check):

```bash
pytest -q -W error
```

## Data Notes

- Raw source files are stored under `archive/` (ignored by git due to size).
- Processed files used by the app are stored under `data/`.
