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


class OrderProducts(Base):
    __tablename__ = "orderproducts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Add autoincrement=True
    request_id = Column(Integer, ForeignKey("requests.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Integer, nullable=True)
    confirmed = Column(Boolean, default=False)
    deny_reason = Column(String, nullable=True)
    orpr_product = relationship("Products", back_populates="product_orpr")
    orpr_request = relationship("Requests", back_populates="request_orpr")