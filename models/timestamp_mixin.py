from datetime import datetime
from sqlmodel import Field, SQLModel

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())