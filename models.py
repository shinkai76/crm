# encoding=utf-8
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine, DateTime, Float, Unicode
from sqlalchemy.dialects.postgresql import JSON, ARRAY, INTERVAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

# 创建对象的基类:
Base = declarative_base()

def to_dict(self):
    result = ObjectDict()
    for c in self.__table__.columns:
        value = getattr(self, c.name, None)
        if isinstance(c.type, DateTime):
            if value:
                if type(value) != unicode:
                    result[c.name] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    result[c.name] = value
            else:
                result[c.name] = value
        elif isinstance(c.type, Float):
            if value:
                result[c.name] = float(value)
            else:
                result[c.name] = value
        else:
            result[c.name] = value
    return result
 
Base.to_dict = to_dict


class SetOfBook(Base):
    __tablename__ = 'set_of_books'

    id = Column(Integer, primary_key=True)
    set_of_book = Column(Unicode(20))
    default_store_id = Column(Integer)
    default_bill_type = Column(Integer)
    created_at = Column(DateTime)
    created_user = Column(Unicode(20))
    updated_at = Column(DateTime)
    updated_user = Column(Unicode(20))
    user_token = Column(Unicode(200))

set_of_books = SetOfBook.__table__



class CrmContract(Base):
    __tablename__ = 'crm_contracts'

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer)
    category = Column(Unicode(20))
    category_mapped = Column(Unicode(20))
    status = Column(Unicode(20))
    status_mapped = Column(Unicode(20))
    title = Column(Unicode(200))
    total_amount = Column(Float)
    sign_date = Column(DateTime)
    sn = Column(Unicode(50))
    approve_status = Column(Unicode(20))
    approve_status_i18n = Column(Unicode(20))
    owned_department = Column(MutableDict.as_mutable(JSON))
    product_assets_for_new_record = Column(MutableDict.as_mutable(JSON))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator = Column(MutableDict.as_mutable(JSON))
    customer = Column(MutableDict.as_mutable(JSON))
    is_imported = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    imported_at = Column(DateTime)
    imported_user = Column(Unicode(50))
    download_at = Column(DateTime)
    download_user = Column(Unicode(50))
    sale_document_id = Column(Integer)
    sale_document_code = Column(Unicode(50))
    department_id = Column(Integer)
    partner_id = Column(Integer)
    employee_id = Column(Integer)
    set_of_book = Column(Unicode(20))

crm_contracts = CrmContract.__table__

