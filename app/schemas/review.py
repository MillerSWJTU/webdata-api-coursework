from pydantic import BaseModel, Field, ConfigDict


class ReviewBase(BaseModel):
    score: float = Field(ge=0, le=5, description="User score, must be between 0 and 5")
    user_id: str | None = Field(default=None, description="Unique identifier of the reviewer")
    profile_name: str | None = Field(default=None, description="Profile name or nickname of the reviewer")
    summary: str | None = Field(default=None, max_length=255, description="Review summary or title, max 255 characters")
    review_text: str | None = Field(default=None, description="Detailed review textual content")
    review_time: str | None = Field(default=None, description="Time or timestamp of the review")


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)
