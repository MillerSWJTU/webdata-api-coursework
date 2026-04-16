from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import verify_api_key
from app.crud import book as book_crud
from app.crud import review as review_crud
from app.db.database import get_db
from app.schemas.review import ReviewCreate, ReviewRead

router = APIRouter()


@router.get("/{book_id}/reviews", response_model=list[ReviewRead])
def list_book_reviews(
    book_id: int,
    skip: int = Query(default=0, ge=0, description="跳过指定数量的结果 (分页)"),
    limit: int = Query(default=20, ge=1, le=100, description="最大返回数量 (分页)"),
    min_score: float | None = Query(default=None, ge=0, le=5, description="最低评分过滤 (如只看4分以上好评)"),
    db: Session = Depends(get_db),
):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return review_crud.list_reviews_for_book(db, book_id, skip=skip, limit=limit, min_score=min_score)


@router.post("/{book_id}/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
def create_book_review(book_id: int, payload: ReviewCreate, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return review_crud.create_review(db, book_id, payload)
