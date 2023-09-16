
from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from datetime import datetime
import pytz 
import uuid
timezonetash = pytz.timezone("Asia/Tashkent")
Base = declarative_base()

class ParentPage(Base):
    __tablename__='parentpage'
    id = Column(Integer,primary_key=True,index=True)
    page_name = Column(String)
    actions=relationship('Pages',back_populates='parentpage')
    
    


class Pages(Base):
    __tablename__='pages'

    id = Column(Integer,primary_key=True,index=True)
    page_name = Column(String)
    action_name = Column(String)
    role = relationship('Roles',back_populates='page')
    parentpage_id = Column(Integer,ForeignKey('parentpage.id'))
    parentpage = relationship('ParentPage',back_populates='actions')



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
    time_created = Column(DateTime(timezone=True),default=func.now())
    full_name = Column(String,nullable=True)
    status = Column(Integer,default=0)
    sphere_status= Column(Integer,default=0)
    email = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    group_id = Column(Integer,ForeignKey('groups.id'),nullable=True)
    group = relationship('Groups',back_populates='user')
    brigader = relationship('Brigada',back_populates='user')
    brigada_id = Column(Integer,ForeignKey('brigada.id'),nullable=True)
    telegram_id = Column(BIGINT,nullable=True,unique=True)
    request = relationship('Requests',back_populates='user')
    expanditure = relationship('Expanditure',back_populates='user')
    comments = relationship('Comments',back_populates='user')



class ParentFillials(Base):
    __tablename__='parentfillials'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    latitude = Column(Float,nullable=True)
    longtitude = Column(Float,nullable=True)
    country = Column(String)
    status = Column(Integer,default=0)
    fillial_department = relationship('Fillials',back_populates='parentfillial')
    is_fabrica = Column(Integer,nullable=True)





class Fillials(Base):
    __tablename__ = 'fillials'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    request = relationship('Requests',back_populates='fillial')
    parentfillial = relationship('ParentFillials',back_populates='fillial_department')
    parentfillial_id = Column(UUID(as_uuid=True),ForeignKey('parentfillials.id'))
    origin = Column(Integer,default=0)
    status = Column(Integer,default=0)
    supplier = relationship('Suppliers',back_populates='store')


class Suppliers(Base):
    __tablename__='suppliers'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    code = Column(String,nullable=True)
    name = Column(String)
    taxpayernum = Column(Integer)
    store_id = Column(UUID(as_uuid=True),ForeignKey('fillials.id'))
    store = relationship('Fillials',back_populates='supplier')



class Category(Base):
    __tablename__='category'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description =Column(String)
    request = relationship('Requests',back_populates='category')
    status = Column(Integer,default=0)
    urgent = Column(Boolean)
    sphere_status= Column(Integer,nullable=True)
    department=Column(Integer)
    sub_id = Column(Integer,nullable=True)


class Brigada(Base):
    __tablename__ = 'brigada'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String,nullable=True)
    request = relationship('Requests',back_populates='brigada')
    user =relationship('Users',back_populates='brigader',uselist=True)
    status = Column(Integer,default=0)
    created_at = Column(DateTime(timezone=True),default=func.now())
    sphere_status = Column(Integer,default=1)
    
    



class Expanditure(Base):
    __tablename__='expanditure'
    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Integer)
    request = relationship('Requests',back_populates='expanditure')
    request_id = Column(Integer,ForeignKey('requests.id'))
    tool = relationship('Tools',back_populates='expanditure')
    tool_id = Column(Integer,ForeignKey('tools.id'))
    status = Column(Integer,default=0)
    comment = Column(String,nullable=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('Users',back_populates='expanditure')
    created_at = Column(DateTime(timezone=True),default=func.now())


class Requests(Base):
    __tablename__='requests'
    id = Column(Integer,primary_key=True,index=True)
    product = Column(String,nullable=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True),default=func.now())
    fillial = relationship('Fillials',back_populates='request')
    fillial_id = Column(UUID(as_uuid=True),ForeignKey('fillials.id'))
    category = relationship('Category',back_populates='request')
    category_id = Column(Integer,ForeignKey('category.id'))
    file = relationship('Files',back_populates='request')
    brigada = relationship('Brigada',back_populates='request')
    brigada_id = Column(Integer,ForeignKey('brigada.id'),nullable=True)
    status = Column(Integer,default=0)
    started_at = Column(DateTime,nullable=True)
    finished_at = Column(DateTime,nullable=True)
    rating = Column(Integer,nullable=True)
    deny_reason = Column(String,nullable=True)
    user = relationship('Users',back_populates='request')
    expanditure = relationship("Expanditure",back_populates='request')
    user_id = Column(Integer,ForeignKey('users.id'))
    comments = relationship('Comments',back_populates='request')
    user_manager = Column(String,nullable=True)
    is_bot = Column(Integer,default=1)


class Comments(Base):
    __tablename__='comments'
    id = Column(Integer,primary_key=True,index=True)
    request_id = Column(Integer,ForeignKey('requests.id'))
    request= relationship('Requests',back_populates='comments')
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('Users',back_populates='comments')
    comment = Column(String)

    

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer,primary_key=True,index=True)
    url = Column(String)
    request = relationship('Requests',back_populates='file')
    request_id = Column(Integer,ForeignKey('requests.id'))
    status = Column(Integer,default=0)




class ToolParents(Base):
    __tablename__='toolparents'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    child = relationship('FirstChild',back_populates='childi')
    


class FirstChild(Base):
    __tablename__='firstchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    toolparentid = Column(UUID(as_uuid=True),ForeignKey('toolparents.id'))
    childi = relationship('ToolParents',back_populates='child')
    child = relationship('SecondChild',back_populates='childi')



class SecondChild(Base):
    __tablename__='secondchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('firstchild.id'))
    childi = relationship('FirstChild',back_populates='child')
    child = relationship('ThirdChild',back_populates='childi')


class ThirdChild(Base):
    __tablename__='thirdchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('secondchild.id'))
    childi = relationship('SecondChild',back_populates='child')
    child = relationship('FourthChild',back_populates='childi')

class FourthChild(Base):
    __tablename__='fourthchild'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    name = Column(String)
    category = Column(String,nullable=True)
    description = Column(String,nullable=True)
    parentid = Column(UUID(as_uuid=True),ForeignKey('thirdchild.id'))
    childi = relationship('ThirdChild',back_populates='child')


"""
if otdel_sphere == 1 roznitsa arc sklad, 
if otdel_sphere == 2 fabrica arc sklad
"""

class Tools(Base):
    __tablename__ = 'tools'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=True)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    iikoid = Column(String,unique=True)
    producttype = Column(String,nullable=True)
    price = Column(Float)
    parentid = Column(String)
    mainunit = Column(String,nullable=True)
    expanditure = relationship('Expanditure',back_populates='tool')
    total_price = Column(Float,nullable=True)
    amount_left = Column(Float,nullable=True)
    sklad_id = Column(ARRAY(UUID),default=[])
    last_update = Column(DateTime(timezone=True))
