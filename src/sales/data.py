from sqlalchemy import Table, Column, Integer, Date, DateTime, String, Text, ForeignKey, MetaData
from sqlalchemy.engine import Engine


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

    Table(
        'Sale', meta,
        Column('SourceId', Integer, primary_key=True),
        Column('Id', String(60), primary_key=True),
        Column('SKU', Integer, ForeignKey('Product.SKU'), nullable=False),
        Column('SoldFor', Integer, nullable=False),
        Column('StaffId', Integer, nullable=False),
        Column('Timestamp', DateTime, nullable=False),
        Column('StoreId', Integer, ForeignKey('Store.Id'), nullable=False)
    )

    return meta


def create_tables(engine: Engine):
    meta = _define_meta()
    meta.create_all(bind=engine)
    return meta
