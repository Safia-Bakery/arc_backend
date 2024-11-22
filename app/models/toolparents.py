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


class ToolParents(Base):
    __tablename__ = "toolparents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Integer, default=0)

