from celery import Celery
from datetime import datetime
from models import ProductModel, ReviewModel
from os import getenv
from sqlalchemy import text
# from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlmodel import create_engine, Session, SQLModel

import dotenv
import json
import time

dotenv.load_dotenv()

broker = getenv('CELERY_BROKER')
backend = getenv('CELERY_RESULT_BACKEND')
database_url = getenv('DATABASE_URL')

app = Celery('pipeline', broker=broker, backend=backend)

engine = create_engine(database_url, echo=False)
SQLModel.metadata.create_all(engine)

def upsert_product(session, product_data):
    product = session.query(ProductModel).filter(ProductModel.asin == product_data["asin"]).first()
    if product:
        product.brand = product_data["brand"]
        product.updated_at = product_data["updated_at"]
    else:
        product = ProductModel(**product_data)
        session.add(product)
        session.commit()
    return product.id

@app.task
def ingest(fname: str):
    print(f'Ingesting {fname}')
    with open(fname, 'r') as f:
        data = json.load(f)
    with Session(engine) as session:
        for rec in data:
            product_id = upsert_product(session, {
                "asin": rec["CHILD_ASIN"],
                "brand": rec["PRODUCT_BRAND"],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            title = rec["CUSTOMER_REVIEW_TITLE"]
            description = rec["CUSTOMER_REVIEW_DESCRIPTION"]
            rating = rec["CUSTOMER_REVIEW_RATING"]
            review_rec = ReviewModel(
                product_id=product_id,
                title=title if isinstance(title, str) else '',
                description=description if isinstance(description, str) else '',
                rating=rating if isinstance(rating, (int, float)) else None
            )
            session.add(review_rec)
            session.commit()
    return f'{fname}.ingested'

@app.task
def analyze():
    print('Analyzing data')
    time.sleep(5)
    return 'analysis.json'