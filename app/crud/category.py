from sqlalchemy.orm import Session
from app.models.category import Category


def add_category(
        db: Session,
        name,
        description,
        status,
        urgent,
        sub_id,
        department,
        sphere_status,
        file,
        ftime,
        parent_id,
        is_child,
        telegram_id,
        price
):
    db_add_category = Category(
        name=name,
        description=description,
        status=status,
        urgent=urgent,
        sub_id=sub_id,
        department=department,
        sphere_status=sphere_status,
        file=file,
        ftime=ftime,
        parent_id=parent_id,
        is_child=is_child,
        telegram_id=telegram_id,
        price=price
    )
    db.add(db_add_category)
    db.commit()
    db.refresh(db_add_category)

    return db_add_category


def update_category(
    db: Session,
    id,
    name,
    description,
    status,
    urgent,
    department,
    sub_id,
    sphere_status,
    file,
    ftime,
    parent_id,
    is_child,
    telegram_id,
    price
):
    db_update_category = (
        db.query(Category).filter(Category.id == id).first()
    )
    if db_update_category:
        if name is not None:
            db_update_category.name = name
        if description is not None:
            db_update_category.description = description
        if status is not None:
            db_update_category.status = status
        if urgent is not None:
            db_update_category.urgent = urgent
        if department is not None:
            db_update_category.department = department

        if sub_id is not None:
            db_update_category.sub_id = sub_id
        if sphere_status is not None:
            db_update_category.sphere_status = sphere_status
        if file is not None:
            db_update_category.file = file
        if ftime is not None:
            db_update_category.ftime = ftime
        if parent_id is not None:
            db_update_category.parent_id = parent_id
        if is_child is not None:
            db_update_category.is_child = is_child
        if telegram_id is not None:
            db_update_category.telegram_id = telegram_id
        if price is not None:
            db_update_category.price = price
        db.commit()
        db.refresh(db_update_category)
        return db_update_category

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

