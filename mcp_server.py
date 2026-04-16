"""
MCP (Model Context Protocol) Server for the Books & Reviews API.

This module exposes the core query functions of our FastAPI application
as MCP-compatible Tools, allowing AI assistants (e.g. Claude, Copilot)
to search books, read reviews, and retrieve statistics directly.

Run with:  python -m mcp_server
Or:        mcp dev mcp_server.py
"""

import sys
import os

# Ensure the project root is on the Python path so we can import `app.*`
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.book import Book
from app.models.review import Review

# ── Database setup (reuse the same SQLite file as the main API) ──────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── MCP Server instance ─────────────────────────────────────────────────────
mcp = FastMCP(
    "Books & Reviews MCP Server",
    instructions=(
        "You have access to a books and reviews database (Goodreads data). "
        "Use the provided tools to search for books, get book details, "
        "read user reviews, and retrieve aggregate statistics."
    ),
)


def _get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


# ── Tool 1: Search Books ────────────────────────────────────────────────────
@mcp.tool()
def search_books(
    query: str = "",
    category: str = "",
    skip: int = 0,
    limit: int = 10,
) -> list[dict]:
    """
    Search for books by title keyword and/or category.
    Returns a list of matching books with id, title, authors, categories, and ratings_count.
    Use empty string for query/category to skip that filter.
    """
    db = _get_db()
    try:
        stmt = select(Book)
        if query:
            stmt = stmt.where(Book.title.ilike(f"%{query}%"))
        if category:
            stmt = stmt.where(Book.categories.ilike(f"%{category}%"))
        stmt = stmt.order_by(Book.id).offset(skip).limit(limit)
        books = db.execute(stmt).scalars().all()
        return [
            {
                "id": b.id,
                "title": b.title,
                "authors": b.authors,
                "categories": b.categories,
                "ratings_count": b.ratings_count,
            }
            for b in books
        ]
    finally:
        db.close()


# ── Tool 2: Get Book Details ────────────────────────────────────────────────
@mcp.tool()
def get_book_details(book_id: int) -> dict:
    """
    Get full details of a single book by its ID.
    Returns all fields: id, title, description, authors, publisher,
    published_date, categories, ratings_count.
    """
    db = _get_db()
    try:
        book = db.get(Book, book_id)
        if not book:
            return {"error": f"Book with id {book_id} not found"}
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "authors": book.authors,
            "publisher": book.publisher,
            "published_date": book.published_date,
            "categories": book.categories,
            "ratings_count": book.ratings_count,
        }
    finally:
        db.close()


# ── Tool 3: Get Reviews for a Book ─────────────────────────────────────────
@mcp.tool()
def get_book_reviews(book_id: int, skip: int = 0, limit: int = 5, min_score: float | None = None) -> list[dict]:
    """
    Get user reviews for a specific book.
    Returns a list of reviews with score, profile_name, summary, and review_text.
    Optional min_score filter to get only good reviews.
    """
    db = _get_db()
    try:
        stmt = select(Review).where(Review.book_id == book_id)
        if min_score is not None:
            stmt = stmt.where(Review.score >= min_score)
        
        stmt = stmt.order_by(Review.id.desc()).offset(skip).limit(limit)
        reviews = db.execute(stmt).scalars().all()
        return [
            {
                "id": r.id,
                "score": r.score,
                "profile_name": r.profile_name,
                "summary": r.summary,
                "review_text": r.review_text,
            }
            for r in reviews
        ]
    finally:
        db.close()


# ── Tool 4: Get Database Statistics ─────────────────────────────────────────
@mcp.tool()
def get_stats() -> dict:
    """
    Get aggregate statistics about the books database.
    Returns total_books, total_reviews, and average_ratings_count.
    """
    db = _get_db()
    try:
        total_books = db.scalar(select(func.count(Book.id))) or 0
        total_reviews = db.scalar(select(func.count(Review.id))) or 0
        avg_ratings = db.scalar(select(func.avg(Book.ratings_count))) or 0
        return {
            "total_books": int(total_books),
            "total_reviews": int(total_reviews),
            "average_ratings_count": round(float(avg_ratings), 2),
        }
    finally:
        db.close()


# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
