import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    BIGINT
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


#fillial is departments of fillial bar, arc, etc
class Fillials(Base):
    __tablename__ = "fillials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    request = relationship("Requests", back_populates="fillial")
    parentfillial = relationship("ParentFillials", back_populates="fillial_department")
    parentfillial_id = Column(UUID(as_uuid=True), ForeignKey("parentfillials.id"))
    origin = Column(Integer, default=0)
    status = Column(Integer, default=0)
    supplier = relationship("Suppliers", back_populates="store")
    tool_balance = relationship("ToolBalance", back_populates="store")
    arc = Column(Integer, default=0)
    manager_id = Column(BIGINT, ForeignKey("managers.id"))
    manager = relationship("Managers", back_populates="division")


