from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from .timestamp_mixin import TimestampMixin

class InsightModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "insights"
    id: int = Field(default=None, primary_key=True)
    review_id: int = Field(default=None, foreign_key="reviews.id")
    insights: Optional[dict] = Field(sa_column=Column(JSONB), default=None)
    # insight: str