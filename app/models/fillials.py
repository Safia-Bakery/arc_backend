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
    user = relationship("Users", back_populates="branch")
    kru_finished_task = relationship("KruFinishedTasks", back_populates="branch")
