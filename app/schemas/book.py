from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    authors: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    categories: str | None = None
    ratings_count: int = 0


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    authors: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    categories: str | None = None
    ratings_count: int | None = None


class BookRead(BookBase):
    id: int

    class Config:
        from_attributes = True
