from sqlmodel import Field, SQLModel
from .timestamp_mixin import TimestampMixin

class ProductModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "products"
    id: int = Field(default=None, primary_key=True)
    asin: str = Field(default=None, index=True, nullable=False, unique=True)
    brand: str
