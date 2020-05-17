from sqlalchemy import inspect, Date, Integer, Float, DateTime, String, Text
from sqlalchemy.engine import Engine

from . import data


def test_create_sales(engine: Engine):
    data.create_tables(engine=engine)
    instrument = inspect(engine)

    assert 'Sale' in instrument.get_table_names()

    [source_id, id, sku, discount_percent, staff_id, timestamp, store_id] = instrument.get_columns('Sale')

    assert source_id['name'] == 'SourceId'
    assert isinstance(source_id['type'], Integer)
    assert source_id['primary_key'] == 1

    assert id['name'] == 'Id'
    assert isinstance(id['type'], String)
    assert id['primary_key'] == 2

    assert sku['name'] == 'SKU'
    assert isinstance(sku['type'], Integer)
    assert not sku['nullable']

    assert discount_percent['name'] == 'DiscountPercent'
    assert isinstance(discount_percent['type'], Float)

    assert staff_id['name'] == 'StaffId'
    assert isinstance(staff_id['type'], Integer)
    assert not staff_id['nullable']

    assert timestamp['name'] == 'Timestamp'
    assert isinstance(timestamp['type'], DateTime)

    assert store_id['name'] == 'StoreId'
    assert isinstance(store_id['type'], Integer)
    assert not store_id['nullable']


def test_create_stores(engine: Engine):
    data.create_tables(engine=engine)
    instrument = inspect(engine)

    assert 'Store' in instrument.get_table_names()

    [id, name, postcode, address] = instrument.get_columns('Store')

    assert id['name'] == 'Id'
    assert isinstance(id['type'], Integer)
    assert id['primary_key'] == 1

    assert name['name'] == 'Name'
    assert isinstance(name['type'], String)
    assert not name['nullable']

    assert postcode['name'] == 'Postcode'
    assert isinstance(postcode['type'], String)
    assert not postcode['nullable']

    assert address['name'] == 'Address'
    assert isinstance(address['type'], Text)
    assert not address['nullable']


def test_create_products(engine: Engine):
    data.create_tables(engine=engine)
    instrument = inspect(engine)

    assert 'Product' in instrument.get_table_names()

    [date, sku, price] = instrument.get_columns('Product')

    assert date['name'] == 'Date'
    assert isinstance(date['type'], Date)
    assert date['primary_key'] == 1

    assert sku['name'] == 'SKU'
    assert isinstance(sku['type'], Integer)
    assert sku['primary_key'] == 2

    assert price['name'] == 'Price'
    assert isinstance(sku['type'], Integer)
    assert not price['nullable']
