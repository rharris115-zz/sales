from sqlalchemy import Table, Column, Integer, Date, DateTime, String, Text, ForeignKey, MetaData
from sqlalchemy.engine import Engine
from typing import IO
import json
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'
    date = Column('Date', Date, primary_key=True)
    sku = Column('SKU', Integer, primary_key=True)
    price = Column('Price', Integer, nullable=False)


class Store(Base):
    __tablename__ = 'Store'
    id = Column('Id', Integer, primary_key=True)
    name = Column('Name', String(40), nullable=False)
    postcode = Column('Postcode', String(8), nullable=False)
    address = Column('Address', Text, nullable=False)


class Sale(Base):
    __tablename__ = 'Sale'
    source_id = Column('SourceId', Integer, primary_key=True)
    id = Column('Id', String(60), primary_key=True)
    sku = Column('SKU', Integer, ForeignKey('Product.SKU'), nullable=False)
    sold_for = Column('SoldFor', Integer, nullable=False)
    staff_id = Column('StaffId', Integer, nullable=False)
    timestamp = Column('Timestamp', DateTime, nullable=False)
    store_id = Column('StoreId', Integer, ForeignKey('Store.Id'), nullable=False)


def create_tables(engine: Engine):
    meta = Base.metadata
    meta.create_all(bind=engine)
    return meta


def import_products(products: IO[str]):
    data = json.loads(s=products.read())
    return None
