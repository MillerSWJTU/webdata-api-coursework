from fastapi import APIRouter

from app.api.routes import books, health, reviews

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(reviews.router, prefix="/books", tags=["reviews"])
