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



class Tools(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    iikoid = Column(String, unique=True)
    producttype = Column(String, nullable=True)
    price = Column(Float)
    parentid = Column(String)
    mainunit = Column(String, nullable=True)
    expanditure = relationship("Expanditure", back_populates="tool")
    total_price = Column(Float, nullable=True)
    amount_left = Column(Float, nullable=True)
    sklad_id = Column(ARRAY(UUID(as_uuid=True)), default=[])
    last_update = Column(DateTime(timezone=True))
    department = Column(Integer, nullable=True)
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    image = Column(String, nullable=True)
    factory_image = Column(String,nullable=True)
    ftime = Column(Float, nullable=True)
    tool_need = relationship("NeededTools", back_populates="need_tool")
    status = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("category.id"))
    categories = relationship("Category", back_populates="tool")
    tool_balance = relationship("ToolBalance", back_populates="tool")
    order_item = relationship("CollectOrderItems", back_populates="product")
    category_tools = relationship('CategoriesToolsRelations',back_populates='tool')

