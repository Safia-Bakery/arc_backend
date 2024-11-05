from sqlalchemy.orm import Session
from app.models.tool_balance import ToolBalance
from sqlalchemy import and_


# def filter_requests_all(
#         db: Session,
#         id,
#         user,
#         fillial_id,
#         created_at,
#         request_status,
#         department
# ):
#     query = db.query(Requests).filter(Category.department == department)
#
#     query.options(
#         joinedload(Requests.request_orpr)
#         .joinedload(OrderProducts.orpr_product)
#         .joinedload(Products.prod_cat)
#     )
#
#     if id is not None:
#         query = query.filter(Requests.id == id)
#     if fillial_id is not None:
#         query = query.outerjoin(Fillials).filter(Fillials.parentfillial_id == fillial_id)
#     if created_at is not None:
#         query = query.filter(cast(Requests.created_at, Date) == created_at)
#     if request_status is not None:
#         request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
#         query = query.filter(Requests.status.in_(request_status))
#     if user is not None:
#         query = query.filter(Users.full_name.ilike(f"%{user}%"))
#
#     results = query.order_by(Requests.id.desc()).all()
#     return results


def get_department_product_balances(db: Session, department_id, store_id, tool_id):
    query = db.query(ToolBalance).filter(ToolBalance.store_id == store_id)
    if department_id is not None:
        query = query.filter(ToolBalance.departmentId == department_id)
    if tool_id is not None:
        query = query.filter(ToolBalance.tool_id == tool_id)

    result = query.order_by(ToolBalance.amount.asc()).all()
    return result


def get_product_balance(db: Session, department_id, store_id, product_id):
    query = db.query(ToolBalance).filter(and_(ToolBalance.department_id == department_id,
                                              ToolBalance.store_id == store_id,
                                              ToolBalance.tool_id == product_id)
                                         ).first()
    return query


def update_product_balance(db: Session, product_balance, department):
    query = db.query(ToolBalance).filter(and_(ToolBalance.department_id == department,
                                              ToolBalance.store_id == product_balance['storeId'],
                                              ToolBalance.tool_id == product_balance['productId'])
                                         ).first()
    query.departmentId = department
    query.storeId = product_balance['store'] if 'store' in product_balance else None
    query.productId = product_balance['product'] if 'product' in product_balance else None
    query.amount = product_balance['amount'] if 'amount' in product_balance else None
    query.sum = product_balance['sum'] if 'sum' in product_balance else None
    query.price = (product_balance['sum'] / product_balance[
        'amount']) if 'sum' in product_balance and 'amount' in product_balance and product_balance[
        'amount'] != 0 else None

    db.commit()
    return True


def create_product_balance(db: Session, product_balance, department):
    query = ToolBalance(
        department_id=department,
        store_id=product_balance['storeId'] if 'storeId' in product_balance else None,
        tool_id=product_balance['productId'] if 'productId' in product_balance else None,
        amount=product_balance['amount'] if 'amount' in product_balance else None,
        sum=product_balance['sum'] if 'sum' in product_balance else None,
        price=(product_balance['sum'] / product_balance['amount']) if 'sum' in product_balance and
                                                                      'amount' in product_balance and
                                                                      product_balance['amount'] != 0 else None
    )

    db.add(query)
    db.commit()
    return True


def create_update_tool_balance(db: Session, data, department):
    for product_balance in data:
        is_product_exists = get_product_balance(db, department, product_balance['storeId'], product_balance['productId'])
        if is_product_exists:
            update_product_balance(db, product_balance, department)
        else:
            create_product_balance(db, product_balance, department)

    return True
