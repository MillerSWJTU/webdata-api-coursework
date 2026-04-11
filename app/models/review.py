from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(60), nullable=True)
    profile_name: Mapped[str] = mapped_column(String(120), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=True)
    review_text: Mapped[str] = mapped_column(Text, nullable=True)
    review_time: Mapped[str] = mapped_column(String(30), nullable=True)

    book = relationship("Book", back_populates="reviews")
