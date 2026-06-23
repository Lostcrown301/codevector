from sqlalchemy import Column, String, Float, DateTime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
