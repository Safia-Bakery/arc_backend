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



class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    request = relationship("Requests", back_populates="category")
    status = Column(Integer, default=0)
    urgent = Column(Boolean)
    sphere_status = Column(Integer, nullable=True)
    department = Column(Integer)
    department_name = Column(String, nullable=True)
    sphere_status_name = Column(String,nullable=True)
    sub_id = Column(Integer, nullable=True)
    sub_name = Column(String, nullable=True)
    file = Column(String, nullable=True)
    ftime = Column(Float, nullable=True)
    cat_prod = relationship("Products", back_populates="prod_cat")
    parent_id = Column(Integer, nullable=True)
    price = Column(Float,nullable=True)
    is_child = Column(Boolean,default=False)
    telegram_id = Column(Integer,ForeignKey("telegrams.id"),nullable=True)
    universal_size = Column(Boolean, nullable=True)
    telegram = relationship("Telegrams", back_populates="categories")
    tool = relationship("Tools", back_populates="categories")
    categories_relations = relationship("CategoriesToolsRelations",back_populates='categories')
