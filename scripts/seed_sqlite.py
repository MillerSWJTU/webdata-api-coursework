import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.models.book import Book
from app.models.review import Review

BASE = Path(__file__).resolve().parents[1]
BOOKS_CSV = BASE / "data" / "books_cleaned.csv"
REVIEWS_CSV = BASE / "data" / "reviews_cleaned.csv"


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def seed_books(db: Session) -> dict[str, int]:
    title_to_id: dict[str, int] = {}
    with open(BOOKS_CSV, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            book = Book(
                title=row["title"],
                description=row.get("description") or None,
                authors=row.get("authors") or None,
                publisher=row.get("publisher") or None,
                published_date=row.get("published_date") or None,
                categories=row.get("categories") or None,
                ratings_count=to_int(row.get("ratings_count", "0")),
            )
            db.add(book)
            db.flush()
            title_to_id[book.title] = book.id
    db.commit()
    return title_to_id


def seed_reviews(db: Session, title_to_id: dict[str, int]) -> int:
    count = 0
    with open(REVIEWS_CSV, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            book_id = title_to_id.get(row.get("book_title", ""))
            if not book_id:
                continue
            review = Review(
                book_id=book_id,
                user_id=(row.get("user_id") or None),
                profile_name=(row.get("profile_name") or None),
                score=to_float(row.get("score", "0")),
                summary=(row.get("summary") or None),
                review_text=(row.get("review_text") or None),
                review_time=(row.get("review_time") or None),
            )
            db.add(review)
            count += 1
    db.commit()
    return count


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        db.query(Review).delete()
        db.query(Book).delete()
        db.commit()

        title_to_id = seed_books(db)
        review_count = seed_reviews(db, title_to_id)
        print(f"Seed completed: {len(title_to_id)} books, {review_count} reviews")
    finally:
        db.close()


if __name__ == "__main__":
    main()
