from sqlmodel import Field, SQLModel

class ProductInsightModel(SQLModel, table=False):
    __tablename__ = "product_insights"
    id: int = Field(primary_key=True)
    asin: str
    brand: str
    reviews: int
    positives: int
    negatives: int
    neutrals: int

"""
    select
        p.id,
        asin,
        brand,
        (select count(*) from reviews where product_id = p.id) reviews,
        (select count(*) from sentiments where sentiment = 'positive' and review_id in (select id from reviews where product_id = p.id)) positives,
        (select count(*) from sentiments where sentiment = 'negative' and review_id in (select id from reviews where product_id = p.id)) negatives,
        (select count(*) from sentiments where sentiment = 'neutral' and review_id in (select id from reviews where product_id = p.id)) neutrals
    from products p;
"""