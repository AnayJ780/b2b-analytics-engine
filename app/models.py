from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import DateTime
from datetime import datetime

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, index=True)
    api_key = Column(String) # We store the hashed password here

    # FIXED: Replaced 'products' and 'Product' to match our analytics logic
    sales = relationship("SalesRecord", back_populates="merchant")


class SalesRecord(Base):
    __tablename__ = "sales_records"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    quantity_sold = Column(Integer)
    revenue = Column(Float)
    
    # This Foreign Key enforces Tenant Isolation in the database
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    pload_timestamp = Column(DateTime, default=datetime.utcnow)
    # FIXED: Points back to the Merchant table 
    merchant = relationship("Merchant", back_populates="sales")