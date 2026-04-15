from pydantic import BaseModel, Field, ConfigDict


class ReviewBase(BaseModel):
    score: float = Field(ge=0, le=5, description="用户给出的评分，必须在0到5之间")
    user_id: str | None = Field(default=None, description="写评论的用户唯一标识符")
    profile_name: str | None = Field(default=None, description="写评论的用户昵称")
    summary: str | None = Field(default=None, max_length=255, description="评论摘要或标题，不能过长")
    review_text: str | None = Field(default=None, description="详细的评论内容")
    review_time: str | None = Field(default=None, description="评论发布的时间、时间戳或文本")


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)
