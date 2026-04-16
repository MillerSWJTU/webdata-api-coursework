# webdata-api-coursework

Data-driven RESTful API built with FastAPI, SQLite and Swagger for XJCO3011 coursework.

🚀 **Live Deployment**: [https://webdata-api-coursework.onrender.com](https://webdata-api-coursework.onrender.com)
📄 **Static API Documentation (PDF)**: [docs/API.pdf](./docs/API.pdf)

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- Swagger (OpenAPI) auto docs

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
```

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies.
3. Seed SQLite from cleaned CSV files.
4. Run API server.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
py -3 -m scripts.seed_sqlite
uvicorn app.main:app --reload
```

## API Docs

**Live Online Documentation:**
- Swagger UI (Interactive): [https://webdata-api-coursework.onrender.com/docs](https://webdata-api-coursework.onrender.com/docs)
- ReDoc (Detailed): [https://webdata-api-coursework.onrender.com/redoc](https://webdata-api-coursework.onrender.com/redoc)

**Local Development Documentation (When running `uvicorn`):**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Current Endpoints

- `GET /api/health`
- `GET /api/books`
- `GET /api/books/stats`
- `GET /api/books/{book_id}`
- `POST /api/books`
- `PUT /api/books/{book_id}`
- `DELETE /api/books/{book_id}`
- `GET /api/books/{book_id}/reviews`
- `POST /api/books/{book_id}/reviews`

## Data Notes

- Raw source files are stored under `archive/` (ignored by git due to size).
- Processed files used by the app are stored under `data/`.
