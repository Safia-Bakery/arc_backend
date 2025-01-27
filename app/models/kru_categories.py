from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Time,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base



class KruCategories(Base):
    __tablename__ = "kru_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    status = Column(Integer, default=1)
    parent = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    kru_task = relationship("KruTasks", back_populates="kru_category")
    tool_id = Column(Integer, ForeignKey("tools.id"))
    tool = relationship("Tools", back_populates="kru_category")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
