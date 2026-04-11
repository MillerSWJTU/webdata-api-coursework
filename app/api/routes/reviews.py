from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import book as book_crud
from app.crud import review as review_crud
from app.db.database import get_db
from app.schemas.review import ReviewCreate, ReviewRead

router = APIRouter()


@router.get("/{book_id}/reviews", response_model=list[ReviewRead])
def list_book_reviews(
    book_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return review_crud.list_reviews_for_book(db, book_id, limit=limit)


@router.post("/{book_id}/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_book_review(book_id: int, payload: ReviewCreate, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return review_crud.create_review(db, book_id, payload)
