from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.tool_balance import ToolBalance
from app.models.tools import Tools
from app.models.toolparents import ToolParents
from sqlalchemy import and_

from app.schemas.tool_balance import UpdateToolBalance


def get_department_product_balances(db: Session, department_id, tool_id):
    query = db.query(ToolBalance).filter(ToolBalance.department_id == department_id)
    if tool_id is not None:
        query = query.filter(ToolBalance.tool_id == tool_id)

    result = query.all()
    return result


def get_department_store_product_balances(db: Session, department_id, store_id, tool_id):
    query = db.query(ToolBalance).filter(ToolBalance.store_id == store_id)
    if department_id is not None:
        query = query.filter(ToolBalance.departmentId == department_id)
    if tool_id is not None:
        query = query.filter(ToolBalance.tool_id == tool_id)

    result = query.order_by(ToolBalance.amount.asc()).all()
    return result


def get_product_balance(db: Session, store_id, product_id):
    query = db.query(ToolBalance).filter(
        and_(
            ToolBalance.store_id == store_id,
            ToolBalance.tool_id == product_id
        )
    ).first()
    return query


def update_product_balance(db: Session, obj, amount, sum, price):
    obj.amount = amount
    obj.sum = sum
    obj.price = price

    db.commit()
    return obj


def create_product_balance(db: Session, department, store_id, tool_id, amount, sum, price, product_iiko):
    query = ToolBalance(
        department_id=department,
        store_id=store_id,
        tool_id=tool_id,
        amount=amount,
        sum=sum,
        price=price
    )
    try:
        db.add(query)
        db.commit()
    except IntegrityError:
        print(f"Was canceled due to UniqueError:\n"
              f"department_id: {query.department_id}\n"
              f"store_id: {query.store_id}\n"
              f"tool_id: {query.tool_id}\n"
              f"tool_iiko_id: {product_iiko}\n"
              )
        db.rollback()


def create_update_tool_balance(db: Session, data_list, department):
    for product_balance in data_list:
        tool_obj = db.query(Tools).filter(Tools.iikoid == product_balance['productId']).first()
        tool_id = tool_obj.id if tool_obj else None
        store_id = product_balance['storeId'] if 'storeId' in product_balance else None
        amount = product_balance['amount'] if 'amount' in product_balance else None
        sum = product_balance['sum'] if 'sum' in product_balance else None
        price = (product_balance['sum'] / product_balance['amount']) if 'sum' in product_balance and 'amount' in product_balance and product_balance['amount'] != 0 else None

        store_product = get_product_balance(db, store_id, tool_id)
        if store_product:
            update_product_balance(db, store_product, amount, sum, price)
        else:
            if store_id is not None and tool_id is not None:
                create_product_balance(db, department, store_id, tool_id, amount, sum, price, product_balance['productId'])


def get_balance(db: Session, department_id, tool_id):
    query = db.query(ToolBalance).filter(
        and_(
            ToolBalance.department_id == department_id,
            ToolBalance.tool_id == tool_id
        )
    ).first()
    return query


def update_balance(db: Session, obj, amount):
    obj.amount = amount
    db.commit()
    db.refresh(obj)
    return obj


def create_balance(db: Session, department, tool_id, amount):
    query = ToolBalance(
        department_id=department,
        tool_id=tool_id,
        amount=amount
    )
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        print(f"Was canceled due to UniqueError:\n"
              f"department_id: {query.department_id}\n"
              f"tool_id: {query.tool_id}\n"
              )
        db.rollback()

    return query


def create_update_balance(db: Session, data: UpdateToolBalance, department_id):
    product_obj = get_balance(db, department_id, data.tool_id)
    if product_obj:
        product_obj = update_balance(db, product_obj, data.amount)
    else:
        product_obj = create_balance(db, department_id, data.tool_id, data.amount)

    return product_obj


def getarchtools(db: Session, parent_id):
    query = db.query(ToolParents).filter(
        and_(
            ToolParents.parent_id == parent_id,
            ToolParents.status == 1
        )
    )
    return query.all()


def tools_query_iarch(db: Session, parent_id, name, branch_id):
    if parent_id is not None or name is not None:
        query = db.query(Tools, ToolBalance).join(
            ToolBalance, Tools.id == ToolBalance.tool_id, isouter=True
        ).filter(
            (ToolBalance.department_id == branch_id) | (ToolBalance.department_id == None)
        )
        if name is not None:
            query = query.filter(Tools.name.ilike(f"%{name}%"))
        if parent_id is not None:
            query = query.filter(Tools.parentid == str(parent_id)).filter(Tools.status == 1)

        query = query.all()

        ready_data = []
        for tool in query:
            tool[0].tool_balances = tool[1]
            ready_data.append(tool[0])
        return ready_data
    else:
        query = []

    return query
