from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class CollectOrders(Base):
    __tablename__ = "collector_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("parentfillials.id"), nullable=True)
    status = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    accepted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    branch = relationship("ParentFillials", back_populates="collector_order")
    order_item = relationship("CollectOrderItems", back_populates="order")
    created_user = relationship(
        "Users",
        foreign_keys=[created_by],
        back_populates="created_orders"
    )
    accepted_user = relationship(
        "Users",
        foreign_keys=[accepted_by],
        back_populates="accepted_orders"
    )


class CollectOrderItems(Base):
    __tablename__ = "collector_order_items"
    order_id = Column(Integer, ForeignKey("collector_orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("tools.id"), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    order = relationship("CollectOrders", back_populates="order_item")
    product = relationship("Tools", back_populates="order_item")
