from sqlalchemy import text
from database import engine

with engine.connect() as conn:

    conn.execute(
        text("""
        CREATE INDEX IF NOT EXISTS idx_products_feed
        ON products(created_at DESC, id DESC)
        """)
    )

    conn.execute(
        text("""
        CREATE INDEX IF NOT EXISTS idx_products_category_feed
        ON products(category, created_at DESC, id DESC)
        """)
    )

    conn.commit()

print("Indexes created successfully!")