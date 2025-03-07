from datetime import datetime
from sqlmodel import Field, SQLModel
from .timestamp_mixin import TimestampMixin
from typing import Optional

class RunModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "runs"
    id: int = Field(default=None, primary_key=True)
    filename: str
    stopped_at: Optional[datetime] = Field(default=None)