from database import SessionLocal
from models import Product
from uuid import uuid4
from datetime import datetime

db = SessionLocal()

for i in range(50):
    db.add(
        Product(
            id=str(uuid4()),
            name=f"New Product {i}",
            category="Electronics",
            price=999,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    )

db.commit()

print("Inserted 50 products")