from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.tool_balance import ToolBalance
from app.models.tools import Tools
from app.models.category import Category
from sqlalchemy import and_


# def get_tool_balances(db: Session, department_id, category_id, tool_name):
#     query = db.query(ToolBalance).filter(ToolBalance.department_id == department_id)
#     if category_id is not None:
#         query = query.join(Tools).join(Category).filter(Category.id == category_id)
#     if tool_name is not None:
#         query = query.filter(Tools.name.ilike(f"%{tool_name}%"))
#
#     result = query.order_by(Tools.name.asc()).all()
#     return result


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
    # query = db.query(ToolBalance).filter(
    #     and_(
    #         ToolBalance.store_id == store_id,
    #         ToolBalance.tool_id == product_id
    #     )
    # ).first()

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

