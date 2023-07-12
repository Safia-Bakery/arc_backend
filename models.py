from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz 

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
    username = Column(String, unique=True, index=True)
    password = Column(String)
    time_created = Column(DateTime,default=datetime.now(timezonetash))
    full_name = Column(String,nullable=True)
    status = Column(Integer,default=0)
    email = Column(String,unique=True,nullable=True)
    phone_number = Column(String,nullable=True)
    
    group_id = Column(Integer,ForeignKey('groups.id'),nullable=True)
    group = relationship('Groups',back_populates='user')
    brigader = relationship('Brigada',back_populates='user')
    brigada_id = Column(Integer,ForeignKey('brigada.id'))









class Fillials(Base):
    __tablename__ = 'fillials'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    latitude = Column(Float,nullable=True)
    longtitude = Column(Float,nullable=True)
    country = Column(String)
    request = relationship('Requests',back_populates='fillial')
    status = Column(Integer,default=0)


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
    user =relationship('Users',back_populates='brigader')
    status = Column(Integer,default=0)
    




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
    finished_at = Column(DateTime,nullable=True)
    usertg_phone = Column(String,nullable=True,default='manager')
    usertg_id = Column(BIGINT,nullable=True)
    rating = Column(Integer,nullable=True)
    department = Column(Integer,nullable=True)
    urgent = Column(Boolean)

    

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer,primary_key=True,index=True)
    url = Column(String)
    request = relationship('Requests',back_populates='file')
    request_id = Column(Integer,ForeignKey('requests.id'))


