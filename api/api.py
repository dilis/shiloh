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
CREATE OR REPLACE VIEW product_insights AS
    SELECT
        p.id,
        p.asin,
        p.brand,
        (SELECT COUNT(*) FROM reviews WHERE product_id = p.id) AS reviews,
        (SELECT COUNT(*) FROM sentiments WHERE sentiment = 'positive' AND review_id IN (SELECT id FROM reviews WHERE product_id = p.id)) AS positives,
        (SELECT COUNT(*) FROM sentiments WHERE sentiment = 'negative' AND review_id IN (SELECT id FROM reviews WHERE product_id = p.id)) AS negatives,
        (SELECT COUNT(*) FROM sentiments WHERE sentiment = 'neutral' AND review_id IN (SELECT id FROM reviews WHERE product_id = p.id)) AS neutrals,
        (SELECT jsonb_agg(element) FROM (
            SELECT jsonb_array_elements_text(insights) AS element
            FROM insights
            WHERE review_id IN (SELECT id FROM reviews WHERE product_id = p.id)
        ) AS elements) AS insights
    FROM products p;
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
    print(f'page: {page}, page_size: {page_size}')
    async with AsyncSession(engine) as session:
        stmt = select(ProductModel).limit(page_size).offset((page - 1) * page_size)
        result = await session.execute(stmt)
        products = result.scalars().all()
    return [product.model_dump() for product in products]