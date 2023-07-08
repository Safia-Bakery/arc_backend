from sqlalchemy.orm import Session

import models
import schemas
import bcrypt



def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()




def create_user(db:Session,user : schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.Users(username=user.username.lower(), password=hashed_password,full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_roles(db:Session):
    return db.query(models.Pages).all()


def create_group(db:Session,group:schemas.CreateGroupSch):
    group_user = models.Groups(name=group.name)
    db.add(group_user)
    db.commit()
    db.refresh(group_user)
    return group_user
def get_group(db:Session):
    return db.query(models.Groups).all()
def get_permissions(db:Session,id):
    data = db.query(models.Roles).filter(models.Roles.group_id==id).all()
    return data
def delete_roles(db:Session,id):
    db.query(models.Roles).filter(models.Roles.group_id==id).delete()
    db.commit()
    return True

def bulk_create_per(db:Session,per_obj):
    db.bulk_save_objects(per_obj)
    db.commit()
    return True
