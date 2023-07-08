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
    telegram_id = Column(BIGINT,unique=True,nullable=True)
    
    group_id = Column(Integer,ForeignKey('groups.id'),nullable=True)
    group = relationship('Groups',back_populates='user')





