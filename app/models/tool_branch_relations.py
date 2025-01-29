from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ToolBranchCategoryRelation(Base):
    __tablename__ = "tool_branch_relation"
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey('tools.id'))
    tool = relationship("Tools", back_populates="tool_branches")
    branch_id = Column(UUID, ForeignKey('parentfillials.id'))
    branch = relationship("ParentFillials", back_populates="branch_tools")
    kru_category_id = Column(Integer, ForeignKey('kru_categories.id'))
    kru_category = relationship("KruCategories", back_populates="category_branches")
    created_at = Column(DateTime(timezone=True), default=func.now())
