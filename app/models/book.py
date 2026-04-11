from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    authors: Mapped[str] = mapped_column(String(255), nullable=True)
    publisher: Mapped[str] = mapped_column(String(120), nullable=True)
    published_date: Mapped[str] = mapped_column(String(30), nullable=True)
    categories: Mapped[str] = mapped_column(String(120), nullable=True, index=True)
    ratings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
