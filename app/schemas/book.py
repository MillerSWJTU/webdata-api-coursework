from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255, description="Book title, max 255 characters")
    description: str | None = Field(default=None, description="Detailed description or synopsis of the book")
    authors: str | None = Field(default=None, description="Authors, comma-separated for multiple")
    publisher: str | None = Field(default=None, description="Publisher name")
    published_date: str | None = Field(default=None, description="Published date (e.g., 1999-12-01)")
    categories: str | None = Field(default=None, description="Book categories (e.g., Fiction, Computers)")
    ratings_count: int = Field(default=0, ge=0, description="Total number of ratings")


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

    model_config = ConfigDict(from_attributes=True)
