from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
String

)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Managers(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=True)
    description = Column(String,nullable=True)
    division = relationship("Fillials", back_populates="manager")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

