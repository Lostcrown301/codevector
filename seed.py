from faker import Faker
from uuid import uuid4
from datetime import datetime, timedelta
import random

from database import SessionLocal
from models import Product
from sqlalchemy import text

fake = Faker()

db = SessionLocal()

categories = [
    "Electronics",
    "Books",
    "Clothing",
    "Sports",
    "Home"
]

products = []

# Clear old data
# db.execute(text("TRUNCATE TABLE products"))
# db.commit()

# print("Old products removed")


# New data
TOTAL_PRODUCTS = 200000
BATCH_SIZE = 5000

for batch_start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):

    products = []

    for i in range(batch_start, min(batch_start + BATCH_SIZE, TOTAL_PRODUCTS)):

        product = Product(
            id=str(uuid4()),
            name=f"Product {i:06d}",
            category=random.choice(categories),
            price=random.randint(100, 10000),
            created_at=datetime.utcnow() -
            timedelta(days=random.randint(0, 365)),
            updated_at=datetime.utcnow()
        )

        products.append(product)

    db.bulk_save_objects(products)
    db.commit()

    print(
        f"Inserted {batch_start + len(products)} "
        f"of {TOTAL_PRODUCTS}"
    )