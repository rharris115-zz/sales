from sqlalchemy import Column, Integer, Numeric, Date, DateTime, String, Text, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'Products'
    date = Column('Date', Date, primary_key=True)
    sku = Column('SKU', Integer, primary_key=True)
    price = Column('Price', Numeric(scale=2, precision=9), nullable=False)


class Store(Base):
    __tablename__ = 'Stores'
    id = Column('Id', Integer, primary_key=True)
    name = Column('Name', String(40), nullable=False)
    postcode = Column('Postcode', String(8), nullable=False)
    address = Column('Address', Text, nullable=False)


class Sale(Base):
    __tablename__ = 'Sales'
    id = Column('Id', Integer, primary_key=True)
    sku = Column('SKU', Integer, nullable=False)
    sold_for = Column('SoldFor', Numeric(scale=2, precision=9), nullable=False)
    staff_id = Column('StaffId', Integer, nullable=False)
    timestamp = Column('Timestamp', DateTime, nullable=False)
    store_id = Column('StoreId', Integer, ForeignKey('Stores.Id'), nullable=False)


def create_tables(engine: Engine):
    meta = Base.metadata
    meta.create_all(bind=engine)
