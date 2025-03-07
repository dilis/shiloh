from sqlmodel import Field, SQLModel
from .timestamp_mixin import TimestampMixin

class PromptStatModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "prompt_stats"
    id: int = Field(default=None, primary_key=True)
    review_id: int = Field(default=None, foreign_key="reviews.id")
    language: str
    chat_id: str
    model: str
    prompt_tokens: int
    response_tokens: int
    response_time: float