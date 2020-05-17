from sqlalchemy.engine import Engine
from sqlalchemy import Table, Column, Integer, Date, String, Text, ForeignKey, MetaData


def _define_meta():
    meta = MetaData()

    Table(
        'Product', meta,
        Column('Date', Date, primary_key=True),
        Column('SKU', Integer, primary_key=True),
        Column('Price', Integer, nullable=False)
    )

    Table(
        'Store', meta,
        Column('Id', Integer, primary_key=True),
        Column('Name', String(40), nullable=False),
        Column('Postcode', String(8), nullable=False),
        Column('Address', Text, nullable=False)
    )

    return meta


def create_tables(engine: Engine):
    meta = _define_meta()
    meta.create_all(bind=engine)
    return meta
