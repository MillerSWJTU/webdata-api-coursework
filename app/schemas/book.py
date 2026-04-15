from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255, description="书籍标题，最多255个字符")
    description: str | None = Field(default=None, description="书籍详细描述简介")
    authors: str | None = Field(default=None, description="作者，多人可用逗号分隔")
    publisher: str | None = Field(default=None, description="出版社名称")
    published_date: str | None = Field(default=None, description="出版日期 (如 1999-12-01)")
    categories: str | None = Field(default=None, description="图书类别 (如 Fiction, Computers)")
    ratings_count: int = Field(default=0, ge=0, description="评分总人数")


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
