from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel
from .timestamp_mixin import TimestampMixin
from typing import Optional

class ReviewModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "reviews"
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(default=None, foreign_key="products.id")
    title: Optional[str] = Field(sa_column=Column(Text), default=None)
    description: Optional[str] = Field(sa_column=Column(Text), default=None)
    rating: int
