from sqlmodel import Field, SQLModel
from .timestamp_mixin import TimestampMixin

class SentimentModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "sentiments"
    id: int = Field(default=None, primary_key=True)
    review_id: int = Field(default=None, foreign_key="reviews.id")
    sentiment: str