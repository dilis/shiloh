from .config import config
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import create_engine, select
from typing import Optional, List, Dict
from pydantic import BaseModel
from models import ProductModel, ProductInsightModel

engine = AsyncEngine(create_engine(url=config.API_DATABASE_URL))

async def create_views():
    product_insight_view = """
    create or replace view product_insights as
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

    async with engine.begin() as conn:
        await conn.execute(text(product_insight_view))
        await conn.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_views()
    yield
    pass

app = FastAPI(title="Amazon Product Intelligence",
              lifespan=lifespan)

@app.get("/api/v1/products/{product_id}/insights")
async def get_product_insights(product_id: str):
    """
    Get insights for a specific product
    """
    async with AsyncSession(engine) as session:
        stmt = select(ProductInsightModel).where(ProductInsightModel.asin == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    print(product)
    return product.model_dump()

@app.get("/api/v1/products")
async def get_products(page: int = 1, page_size: int = 50):
    """
    Get all products with pagination
    """
    # TODO: Implement product listing
    # get 1 page of products
    async with AsyncSession(engine) as session:
        stmt = select(ProductModel).limit(page_size).offset((page - 1) * page_size)
        result = await session.execute(stmt)
        products = result.scalars().all()
    return [product.model_dump() for product in products]