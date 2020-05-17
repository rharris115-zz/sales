from sqlalchemy.engine import Engine
from sqlalchemy import Table, Column, Integer, Date, String, ForeignKey, MetaData


def _define_meta():
    meta = MetaData()
    Table(
        'Products', meta,
        Column('Date', Date, primary_key=True),
        Column('SKU', Integer, primary_key=True),
        Column('Price', Integer)
    )
    return meta


def create_tables(engine: Engine):
    meta = _define_meta()
    meta.create_all(bind=engine)
    return meta
