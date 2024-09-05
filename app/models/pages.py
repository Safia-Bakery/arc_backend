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


class Pages(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String)
    action_name = Column(String)
    role = relationship("Roles", back_populates="page")
    parentpage_id = Column(Integer, ForeignKey("parentpage.id"))
    parentpage = relationship("ParentPage", back_populates="actions")