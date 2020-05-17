from sqlalchemy.engine import Engine
from sqlalchemy import Table, Column, Integer, Date, String, ForeignKey, MetaData


def create_products_if_not_exists(engine: Engine):
    meta = MetaData()
    Table(
        'Products', meta,
        Column('Date', Date, primary_key=True),
        Column('SKU', Integer, primary_key=True),
        Column('Price', Integer)
    )
    meta.create_all(bind=engine)
    return meta
