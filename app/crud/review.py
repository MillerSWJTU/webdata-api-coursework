from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate


def list_reviews_for_book(db: Session, book_id: int, *, skip: int = 0, limit: int = 20):
    stmt = (
        select(Review)
        .where(Review.book_id == book_id)
        .order_by(desc(Review.id))
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def create_review(db: Session, book_id: int, payload: ReviewCreate) -> Review:
    obj = Review(book_id=book_id, **payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
