from sqlalchemy.engine import Engine
from sqlalchemy import Table, Column, Integer, Float, Date, DateTime, String, Text, ForeignKey, MetaData


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

    example = {
        "Id": "3902e58b-a9ba-4102-b88b-2a6d4d5adabe",
        "Sku": 2536,
        "DiscountPercent": 0,
        "StaffId": 10390,
        "SoldAtUtc": "2020-05-14T12:24:00Z",
        "Store": "Norwich"
    }

    Table(
        'Sale', meta,
        Column('SourceId', Integer, primary_key=True),
        Column('Id', String(60), primary_key=True),
        Column('SKU', Integer, ForeignKey('Product.SKU'), nullable=False),
        Column('DiscountPercent', Float),
        Column('StaffId', Integer, nullable=False),
        Column('Timestamp', DateTime, nullable=False),
        Column('StoreId', Integer, ForeignKey('Store.Id'), nullable=False)
    )

    return meta


def create_tables(engine: Engine):
    meta = _define_meta()
    meta.create_all(bind=engine)
    return meta
