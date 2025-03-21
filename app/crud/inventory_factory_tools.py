from typing import Optional

from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_, and_, Date, cast
import re
from uuid import UUID
from sqlalchemy.sql import func

from app.models.CategoriesToolsReleations import CategoriesToolsRelations

from app.models.toolparents import ToolParents
from app.models.category import Category
from app.models.tools import Tools
from app.schemas.inventory_tools import UpdateInventoryFactoryTool



def get_tools(db:Session,name:Optional[str]=None,parent_id:Optional[UUID]=None):
    query = db.query(Tools)
    if name is not None:
        query = query.filter(Tools.name.ilike(f"%{name}%"))
    if parent_id is not None:
        query = query.filter(Tools.parentid==str(parent_id))
    return  query.all()


def get_groups(db:Session,name,parent_id):
    query = db.query(ToolParents)
    if name is not None:
        query = query.filter(ToolParents.name.ilike(f"%{name}%"))
    if parent_id is None:
        query = query.filter(ToolParents.id.in_(
           [ '1b55d7e1-6946-4bbc-bf93-542bfdb2b584',
            '09be831f-1201-4b78-9cad-7c94c3363276',
            '0bf90521-ccb3-4301-b7bc-08ad74ee188d']
        ))
    if parent_id is not None:
        query = query.filter(ToolParents.parent_id==parent_id)
    return query.all()



def get_one_tool(db:Session,id):
    query = db.query(Tools).filter(Tools.id==id).first()
    return query


def update_one_tool(db:Session, id, data:UpdateInventoryFactoryTool):
    query = db.query(Tools).filter(Tools.id==id).first()
    if query:
        query.name = data.name
        if data.status is not None:
            query.status = data.status
        if data.factory_ftime is not None:
            query.factory_ftime = data.factory_ftime
        if data.factory_max_amount  is not None:
            query.factory_max_amount = data.factory_max_amount
        if data.factory_min_amount is not None:
            query.factory_min_amount = data.factory_min_amount
        query.factory_image = data.file

        db.commit()
        db.refresh(query)
    return query


def CreateOrUpdateToolCategory(db:Session,tool_id,category_id):
    query = db.query(CategoriesToolsRelations).filter(CategoriesToolsRelations.tool_id==tool_id).first()
    if query and category_id!=0 :
        query.category_id=category_id
        db.commit()
    elif query and category_id==0:
        db.delete(query)
        db.commit()
        query.categories = None
        query.category_id=None
    else:
        query = CategoriesToolsRelations(category_id=category_id,tool_id=tool_id)
        db.add(query)
        db.commit()
    return query






def get_inventory_categories(db:Session, department,status):
    query = db.query(Category).filter(Category.department==department)
    if status is not None:
        query = query.filter(Category.status==status)

    return query.all()




def get_inventory_factory_tools(db:Session,category_id,name,status):
    query = db.query(Tools).join(CategoriesToolsRelations)
    if category_id is not None:
        query = query.filter(CategoriesToolsRelations.category_id==category_id)
    if name is not None:
        query = query.filter(Tools.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(Tools.status==status)

    query = query.filter(CategoriesToolsRelations.tool_id == Tools.id)



    return query.all()


