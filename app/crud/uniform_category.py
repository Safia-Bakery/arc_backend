from sqlalchemy.orm import Session

from app.models.products import Products
from app.models.category import Category
from app.schemas.uniform_category import CreateCategory, UpdateCategory


def add_category(data: CreateCategory, db: Session):
    category_obj = Category(
        name=data.name,
        description=data.description,
        status=data.status,
        urgent=data.urgent,
        department=9,
        price=data.price,
        universal_size=data.universal_size
    )
    db.add(category_obj)
    db.commit()
    db.refresh(category_obj)

    return category_obj


def update_category(data: UpdateCategory, db: Session):
    category_obj = db.query(Category).filter(Category.id == data.id).first()
    if category_obj:
        if data.name is not None:
            category_obj.name = data.name
        if data.price is not None:
            category_obj.price = data.price
        if data.description is not None:
            category_obj.description = data.description
        if data.status is not None:
            category_obj.status = data.status
        if data.urgent is not None:
            category_obj.urgent = data.urgent
        if data.universal_size is not None:
            category_obj.universal_size = data.universal_size

        db.commit()
        db.refresh(category_obj)
        return category_obj

    return False


def filter_category(
    db: Session, category_status, name, department, sub_id, sphere_status,parent_id
):
    query = db.query(Category)
    if category_status is not None:
        query = query.filter(Category.status == category_status)
    if name is not None:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    if sub_id is not None:
        query = query.filter(Category.sub_id == sub_id)
    if department is not None:
        query = query.filter(Category.department == department)
    if sphere_status is not None:
        query = query.filter(Category.sphere_status == sphere_status)
    query = query.filter(Category.parent_id==parent_id)

    return query.order_by(Category.name).all()


def get_category_id(db: Session, id):
    return db.query(Category).filter(Category.id == id).first()


def add_category_products(db: Session, name, category_id, status, image, description):
    query = Products(
        name=name,
        category_id=category_id,
        status=status,
        image=image,
        description=description,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_category_products(db: Session, name, category_id):
    query = db.query(Products).filter(Products.category_id == category_id)
    if name is not None:
        query = query.filter(Products.name.ilike(f"%{name}%"))
    return query.all()


def get_categories(db: Session, name):
    query = db.query(Category).filter(Category.department == 9)
    if name is not None:
        query = query.filter(Category.name.ilike(f"%{name}%"))

    return query.all()
