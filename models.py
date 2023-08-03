from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import pytz 
import uuid
timezonetash = pytz.timezone("Asia/Tashkent")
Base = declarative_base()


class Pages(Base):
    __tablename__='pages'

    id = Column(Integer,primary_key=True,index=True)
    page_name = Column(String)
    role = relationship('Roles',back_populates='page')


class Groups(Base):
    __tablename__='groups'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    role = relationship('Roles',back_populates='group')
    user = relationship('Users',back_populates='group')
    status = Column(Integer)



class Roles(Base):
    __tablename__='roles'

    id = Column(Integer,primary_key=True,index=True)
    group = relationship('Groups',back_populates='role')
    group_id = Column(Integer,ForeignKey('groups.id'))
    page = relationship('Pages',back_populates='role')
    page_id = Column(Integer,ForeignKey('pages.id'))




class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=True)
    password = Column(String,nullable=True)
    time_created = Column(DateTime,default=datetime.now(timezonetash))
    full_name = Column(String,nullable=True)
    status = Column(Integer,default=0)
    email = Column(String,unique=True,nullable=True)
    phone_number = Column(String,nullable=True,unique=True)
    group_id = Column(Integer,ForeignKey('groups.id'),nullable=True)
    group = relationship('Groups',back_populates='user')
    brigader = relationship('Brigada',back_populates='user')
    brigada_id = Column(Integer,ForeignKey('brigada.id'),nullable=True)
    telegram_id = Column(BIGINT,nullable=True,unique=True)
    request = relationship('Requests',back_populates='user')
    



class Fillials(Base):
    __tablename__ = 'fillials'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    latitude = Column(Float,nullable=True)
    longtitude = Column(Float,nullable=True)
    country = Column(String)
    request = relationship('Requests',back_populates='fillial')
    status = Column(Integer,default=0)
    iiko = Column(String)


class Category(Base):
    __tablename__='category'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description =Column(String)
    request = relationship('Requests',back_populates='category')
    status = Column(Integer,default=0)


class Brigada(Base):
    __tablename__ = 'brigada'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String,nullable=True)
    request = relationship('Requests',back_populates='brigada')
    user =relationship('Users',back_populates='brigader',uselist=True)
    status = Column(Integer,default=0)
    expanditure = relationship("Expanditure",back_populates='brigada')
    created_at = Column(DateTime,default=datetime.now(timezonetash))
    



class Expanditure(Base):
    __tablename__='expanditure'
    id = Column(Integer,primary_key=True,index=True)
    amount = Column(String)
    brigada = relationship('Brigada',back_populates='expanditure')
    brigada_id = Column(Integer,ForeignKey('brigada.id'))
    tool = relationship('Tools',back_populates='expanditure')
    tool_id = Column(Integer,ForeignKey('tools.id'))


class Requests(Base):
    __tablename__='requests'
    id = Column(Integer,primary_key=True,index=True)
    product = Column(String)
    description = Column(String)
    created_at = Column(DateTime,default=datetime.now(timezonetash))
    fillial = relationship('Fillials',back_populates='request')
    fillial_id = Column(Integer,ForeignKey('fillials.id'))
    category = relationship('Category',back_populates='request')
    category_id = Column(Integer,ForeignKey('category.id'))
    file = relationship('Files',back_populates='request')
    brigada = relationship('Brigada',back_populates='request')
    brigada_id = Column(Integer,ForeignKey('brigada.id'),nullable=True)
    status = Column(Integer,default=0)
    started_at = Column(DateTime,nullable=True)
    finished_at = Column(DateTime,nullable=True)
    rating = Column(Integer,nullable=True)
    department = Column(Integer,nullable=True)
    urgent = Column(Boolean)
    comment = Column(String,nullable=True)
    user = relationship('Users',back_populates='request')
    user_id = Column(Integer,ForeignKey('users.id'))
    

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer,primary_key=True,index=True)
    url = Column(String)
    request = relationship('Requests',back_populates='file')
    request_id = Column(Integer,ForeignKey('requests.id'))




class ToolParents(Base):
    __tablename__='toolparents'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    firstchildi = relationship('FirstChild',back_populates='toolparentsi')
    


class FirstChild(Base):
    __tablename__='firstchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    toolparentid = Column(UUID(as_uuid=True),ForeignKey('toolparents.id'))
    toolparentsi = relationship('ToolParents',back_populates='firstchildi')
    secondchildi = relationship('SecondChild',back_populates='firstchildi')



class SecondChild(Base):
    __tablename__='secondchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('firstchild.id'))
    firstchildi = relationship('FirstChild',back_populates='secondchildi')
    thirdchildi = relationship('ThirdChild',back_populates='secondchildi')


class ThirdChild(Base):
    __tablename__='thirdchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('secondchild.id'))
    secondchildi = relationship('SecondChild',back_populates='thirdchildi')
    fourthchildi = relationship('FourthChild',back_populates='thirdchildi')

class FourthChild(Base):
    __tablename__='fourthchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('thirdchild.id'))
    thirdchildi = relationship('ThirdChild',back_populates='fourthchildi')



class Tools(Base):
    __tablename__ = 'tools'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    num = Column(String)
    code = Column(String)
    producttype = Column(String,nullable=True)
    parentid = Column(String)
    mainunit = Column(String,nullable=True)
    expanditure = relationship('Expanditure',back_populates='tool')