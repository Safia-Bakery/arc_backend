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




class ArcExpense(Base):
    __tablename__ = "arcexpense"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="arcexpense")
    expensetype_id = Column(Integer, ForeignKey("arcexpensetype.id"))
    expensetype = relationship("ArcExpenseType", back_populates="expense")


