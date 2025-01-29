import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


#there are 2 types of fillials there is parent fillial that show which fillial is
class ParentFillials(Base):
    __tablename__ = "parentfillials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    latitude = Column(Float, nullable=True)
    longtitude = Column(Float, nullable=True)
    country = Column(String)
    status = Column(Integer, default=0)
    fillial_department = relationship("Fillials", back_populates="parentfillial")
    is_fabrica = Column(Integer, nullable=True)
    calendar = relationship('Calendars', back_populates='branch')
    kru_finished_task = relationship("KruFinishedTasks", back_populates="branch")
    user = relationship("Users", back_populates="branch")
    tool_balance = relationship("ToolBalance", back_populates="branch")
    collector_order = relationship("CollectOrders", back_populates="branch")
    appointments = relationship("Appointments", back_populates="branch")
    branch_tools = relationship("ToolBranchCategoryRelation", back_populates="branch")
