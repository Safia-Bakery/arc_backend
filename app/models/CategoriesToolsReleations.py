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



class CategoriesToolsRelations(Base):
    __tablename__ = "category_tools_relations"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer,ForeignKey("category.id"),nullable=True)
    categories = relationship('Category',back_populates='categories_relations')
    tool_id = Column(Integer, ForeignKey('tools.id'),nullable=True)
    tool = relationship('Tools',back_populates='category_tools')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



