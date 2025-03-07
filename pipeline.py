from analyzer import ProductAnalyzer
from celery import Celery
from datetime import datetime
from models import InsightModel, ProductModel, ReviewModel, SentimentModel
from openai import OpenAI
from os import getenv
from sqlalchemy import text
# from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlmodel import create_engine, select, Session, SQLModel

import dotenv
import json
import time

dotenv.load_dotenv()

broker = getenv('CELERY_BROKER')
backend = getenv('CELERY_RESULT_BACKEND')
database_url = getenv('DATABASE_URL')
openai_key = getenv('OPENAI_API_KEY')

app = Celery('pipeline', broker=broker, backend=backend)

engine = create_engine(database_url, echo=False)
SQLModel.metadata.create_all(engine)

# client = OpenAI(api_key=openai_key)
analyzer = ProductAnalyzer(llm_client=OpenAI(api_key=openai_key))

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

def select_and_update_review_status(session: Session):
    with session.begin():
        stmt = select(ReviewModel).where(ReviewModel.status == None).limit(1).with_for_update()
        result = session.exec(stmt).first()
        if result:
            result.status = "pending"
            session.add(result)
            result = result.model_dump()
            session.commit()
            return result
    return None

@app.task
def analyze():
    print('Analyzing data')
    with Session(engine) as session:
        print('Session created')
        review = select_and_update_review_status(session)
        while review:
            print(f'Analyzing review id: {review}')
            analysis = analyzer.analyze_review(review)
            sentiment = SentimentModel(
                review_id=review["id"],
                sentiment=analysis["sentiment"]
            )
            session.add(sentiment)
            if analysis["actionable_insights"]:
                session.add(InsightModel(
                    review_id=review["id"],
                    insights=analysis["actionable_insights"]
                ))
            session.commit()
            print(f'Analysis: {analysis}')
            review = select_and_update_review_status(session)
    return 'analysis.json'