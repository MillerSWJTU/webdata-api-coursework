from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import verify_api_key
from app.crud import book as book_crud
from app.db.database import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter()


@router.get("", response_model=list[BookRead])
def list_books(
    skip: int = Query(default=0, ge=0, description="分页偏移"),
    limit: int = Query(default=20, ge=1, le=100, description="返回数量上限"),
    query: str | None = Query(default=None, description="按书名关键词搜索"),
    category: str | None = Query(default=None, description="按类别过滤"),
    db: Session = Depends(get_db),
):
    return book_crud.list_books(db, skip=skip, limit=limit, query=query, category=category)


@router.get("/stats")
def get_books_stats(db: Session = Depends(get_db)):
    return book_crud.get_books_stats(db)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    return book_crud.create_book(db, payload)


@router.put("/{book_id}", response_model=BookRead, dependencies=[Depends(verify_api_key)])
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book_crud.update_book(db, book, payload)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book_crud.delete_book(db, book)
    return None
