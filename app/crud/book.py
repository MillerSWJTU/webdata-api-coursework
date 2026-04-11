from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def list_books(db: Session, *, skip: int = 0, limit: int = 20, category: str | None = None):
    stmt = select(Book)
    if category:
        stmt = stmt.where(Book.categories.ilike(f"%{category}%"))
    stmt = stmt.order_by(Book.id).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def create_book(db: Session, payload: BookCreate) -> Book:
    obj = Book(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_book(db: Session, book: Book, payload: BookUpdate) -> Book:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()


def get_books_stats(db: Session):
    total_books = db.scalar(select(func.count(Book.id))) or 0
    avg_ratings_count = db.scalar(select(func.avg(Book.ratings_count))) or 0
    return {
        "total_books": int(total_books),
        "average_ratings_count": round(float(avg_ratings_count), 2),
    }
