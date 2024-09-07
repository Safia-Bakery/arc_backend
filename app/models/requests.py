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



class Requests(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, nullable=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    fillial = relationship("Fillials", back_populates="request")
    fillial_id = Column(UUID(as_uuid=True), ForeignKey("fillials.id"), nullable=True)
    category = relationship("Category", back_populates="request")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    file = relationship("Files", back_populates="request")
    brigada = relationship("Brigada", back_populates="request")
    brigada_id = Column(Integer, ForeignKey("brigada.id"), nullable=True)
    status = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    deny_reason = Column(String, nullable=True)
    pause_reason = Column(String, nullable=True)
    user = relationship("Users", back_populates="request")
    expanditure = relationship("Expanditure", back_populates="request")
    user_id = Column(Integer, ForeignKey("users.id"))
    comments = relationship("Comments", back_populates="request")
    user_manager = Column(String, nullable=True)
    is_bot = Column(Integer, default=1)
    size = Column(String, nullable=True)
    arrival_date = Column(DateTime(timezone=True), nullable=True)
    bread_size = Column(String, nullable=True)
    location = Column(JSON, nullable=True)
    update_time = Column(JSONB, nullable=True)
    finishing_time = Column(DateTime(timezone=True), nullable=True)
    is_redirected = Column(Boolean, default=False)
    old_cat_id = Column(Integer, nullable=True)
    request_orpr = relationship("OrderProducts", back_populates="orpr_request")
    cars_id = Column(Integer, ForeignKey("cars.id"), nullable=True)
    cars = relationship("Cars", back_populates="request")
    communication = relationship("Communication", back_populates="requestc")
    price = Column(Float, nullable=True)
    phone_number = Column(String, nullable=True)
    calendar = relationship("Calendars", back_populates="request")