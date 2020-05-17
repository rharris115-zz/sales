import json
from datetime import date
from typing import IO

from sqlalchemy import Column, Integer, Date, DateTime, String, Text, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Product(Base):
    __tablename__ = 'Products'
    date = Column('Date', Date, primary_key=True)
    sku = Column('SKU', Integer, primary_key=True)
    price = Column('Price', Integer, nullable=False)


class Store(Base):
    __tablename__ = 'Stores'
    id = Column('Id', Integer, primary_key=True)
    name = Column('Name', String(40), nullable=False)
    postcode = Column('Postcode', String(8), nullable=False)
    address = Column('Address', Text, nullable=False)


class Sale(Base):
    __tablename__ = 'Sales'
    source_id = Column('SourceId', Integer, primary_key=True)
    id = Column('Id', String(60), primary_key=True)
    sku = Column('SKU', Integer, ForeignKey('Products.SKU'), nullable=False)
    sold_for = Column('SoldFor', Integer, nullable=False)
    staff_id = Column('StaffId', Integer, nullable=False)
    timestamp = Column('Timestamp', DateTime, nullable=False)
    store_id = Column('StoreId', Integer, ForeignKey('Stores.Id'), nullable=False)


def create_tables(engine: Engine):
    meta = Base.metadata
    meta.create_all(bind=engine)


def import_products(date: date, products: IO[str], session: Session):
    data = json.loads(s=products.read())
    instances = [Product(date=date, sku=item['Sku'], price=round(100 * item['Price'])) for item in data]
    session.add_all(instances=instances)
    session.commit()
