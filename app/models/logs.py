from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    status = Column(Integer, nullable=True)
    request = relationship("Requests", back_populates="log")
    user = relationship("Users", back_populates="log")
