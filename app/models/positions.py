from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Positions(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1, nullable=True)
    department = Column(Integer, nullable=True)
    user = relationship("Users", back_populates="position")
    appointments = relationship("Appointments", back_populates="position")
    created_at = Column(DateTime(timezone=True), default=func.now())
