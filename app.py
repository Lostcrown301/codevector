from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import Product
from sqlalchemy import and_, or_
from datetime import datetime
app = FastAPI()

Base.metadata.create_all(bind=engine)

LIMIT = 5

def serialize_product(product):
    return {
        "id" : product.id,
        "name" : product.name,
        "category" : product.category,
        "price" : product.price,
        "created_at" : product.created_at.isoformat(),
        "updated_at" : product.updated_at.isoformat()

    }



@app.get("/")
def home():
    return {"message" : "API Working"}

@app.get("/products")
def get_products(
    limit: int = LIMIT,
    category: str | None = None,
    cursor_created_at: datetime | None = None,
    cursor_id: str | None = None
):
    db = SessionLocal()

    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category == category
        )

    if cursor_created_at and cursor_id:
        query = query.filter(
            or_(
                Product.created_at < cursor_created_at,
                and_(
                    Product.created_at == cursor_created_at,
                    Product.id < cursor_id
                )
            )
        )

    products = (
        query
        .order_by(
            Product.created_at.desc(),
            Product.id.desc()
        )
        .limit(limit)
        .all()
    )

    next_cursor = None

    if products:
        last_product = products[-1]

        next_cursor = {
            "created_at": last_product.created_at.isoformat(),
            "id": last_product.id
        }

    return {
        "products": [serialize_product(product) for product in products],
        "next_cursor": next_cursor
    }

    db.close()
