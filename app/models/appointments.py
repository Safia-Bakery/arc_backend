from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Appointments(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_name = Column(String, nullable=True)
    time_slot = Column(DateTime)
    status = Column(Integer, default=0)
    description = Column(String, nullable=True)
    department = Column(Integer, nullable=True)
    deny_reason = Column(String, nullable=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    schedule = relationship("Schedule", back_populates="appointments")
    position_id = Column(Integer, ForeignKey("positions.id"))
    position = relationship("Positions", back_populates="appointments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="appointments")
    branch_id = Column(UUID(as_uuid=True), ForeignKey('parentfillials.id'))
    branch = relationship('ParentFillials', back_populates='appointments')
    file = relationship("Files", back_populates="appointment")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
