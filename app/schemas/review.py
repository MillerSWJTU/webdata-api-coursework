from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    score: float = Field(ge=0, le=5)
    user_id: str | None = None
    profile_name: str | None = None
    summary: str | None = None
    review_text: str | None = None
    review_time: str | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True
