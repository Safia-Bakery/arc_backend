from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Date,
    Time,
    String,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    time = Column(Time)
    is_available = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    department = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    appointments = relationship("Appointments", back_populates="schedule")

