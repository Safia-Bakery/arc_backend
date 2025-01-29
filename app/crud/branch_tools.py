from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.schemas.branch_tools import CreateToolBranch, DeleteToolBranch
from app.models.tool_branch_relations import ToolBranchCategoryRelation



def create_branch_tools(db: Session, data: CreateToolBranch, branch_id):
    query = db.query(
        ToolBranchCategoryRelation
    ).filter(
        and_(
            ToolBranchCategoryRelation.tool_id == data.tool_id,
            ToolBranchCategoryRelation.branch_id == branch_id
        )
    ).first()
    if not query:
        query = ToolBranchCategoryRelation(
            tool_id=data.tool_id,
            branch_id=branch_id,
            kru_category_id=1
        )
        db.add(query)
        db.commit()
        db.refresh(query)
    else:
        return None

    return query


def get_branch_tools(db: Session, branch_id):
    query = db.query(
        ToolBranchCategoryRelation
    ).filter(
        ToolBranchCategoryRelation.branch_id == branch_id
    ).all()

    return query


def delete_branch_tool(db: Session, body: DeleteToolBranch):
    query = db.query(ToolBranchCategoryRelation).get(ident=body.id)

    if not query:
        return None

    db.delete(query)
    db.commit()
    return {"message": "Item deleted successfully"}