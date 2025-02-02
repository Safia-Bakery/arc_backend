from typing import Optional

from sqlalchemy import and_, asc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.tools import Tools
from app.models.toolparents import ToolParents
from app.schemas.branch_tools import CreateToolBranch, DeleteToolBranch
from app.models.tool_branch_relations import ToolBranchCategoryRelation



def create_branch_tools(db: Session, data: CreateToolBranch):
    created_objs = []
    for tool_id in data.tool_ids:
        query = db.query(
            ToolBranchCategoryRelation
        ).filter(
            and_(
                ToolBranchCategoryRelation.tool_id == tool_id,
                ToolBranchCategoryRelation.branch_id == data.branch_id
            )
        ).first()
        if not query:
            query = ToolBranchCategoryRelation(
                tool_id=tool_id,
                branch_id=data.branch_id,
                kru_category_id=data.category_id
            )
            db.add(query)
            db.commit()
            db.refresh(query)
            created_objs.append(query)

    return created_objs


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



def get_groups(db:Session,name,parent_id):
    query = db.query(ToolParents)
    if name is not None:
        query = query.filter(ToolParents.name.ilike(f"%{name}%"))
    if parent_id is None:
        query = query.filter(ToolParents.id.in_(
           ['1b55d7e1-6946-4bbc-bf93-542bfdb2b584',
            '09be831f-1201-4b78-9cad-7c94c3363276',
            '0bf90521-ccb3-4301-b7bc-08ad74ee188d']
        ))
    if parent_id is not None:
        query = query.filter(ToolParents.parent_id==parent_id)
    return query.all()


def get_tools(db:Session, name:Optional[str]=None):
    query = db.query(Tools)
    if name is not None:
        query = query.filter(Tools.name.ilike(f"%{name}%"))

    return query.order_by(asc(Tools.name)).limit(50).all()