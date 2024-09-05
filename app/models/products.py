from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
from app.db.base import Base
import pytz
import uuid



class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    category_id = Column(Integer, ForeignKey("category.id"))
    status = Column(Integer, default=1)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    prod_cat = relationship("Category", back_populates="cat_prod")
    product_orpr = relationship("OrderProducts", back_populates="orpr_product")
