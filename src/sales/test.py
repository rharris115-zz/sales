from sqlalchemy import inspect, Date, Integer, DateTime, String, Text
from sqlalchemy.engine import Engine

from . import data
from io import StringIO


def test_import_good_product_data(good_product_json_data: str):
    data.import_products(StringIO(good_product_json_data))


def test_create_sales(engine: Engine):
    data.create_tables(engine=engine)
    instrument = inspect(subject=engine)

    assert 'Sales' in instrument.get_table_names()

    [source_id, id, sku, sold_for, staff_id, timestamp, store_id] = instrument.get_columns('Sales')

    assert source_id['name'] == 'SourceId'
    assert isinstance(source_id['type'], Integer)
    assert source_id['primary_key'] == 1

    assert id['name'] == 'Id'
    assert isinstance(id['type'], String)
    assert id['type'].length == 60
    assert id['primary_key'] == 2

    assert sku['name'] == 'SKU'
    assert isinstance(sku['type'], Integer)
    assert not sku['nullable']

    assert sold_for['name'] == 'SoldFor'
    assert isinstance(sold_for['type'], Integer)
    assert not sold_for['nullable']

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

    assert 'Stores' in instrument.get_table_names()

    [id, name, postcode, address] = instrument.get_columns('Stores')

    assert id['name'] == 'Id'
    assert isinstance(id['type'], Integer)
    assert id['primary_key'] == 1

    assert name['name'] == 'Name'
    assert isinstance(name['type'], String)
    assert name['type'].length == 40
    assert not name['nullable']

    assert postcode['name'] == 'Postcode'
    assert isinstance(postcode['type'], String)
    assert postcode['type'].length == 8
    assert not postcode['nullable']

    assert address['name'] == 'Address'
    assert isinstance(address['type'], Text)
    assert not address['nullable']


def test_create_products(engine: Engine):
    data.create_tables(engine=engine)
    instrument = inspect(engine)

    assert 'Products' in instrument.get_table_names()

    [date, sku, price] = instrument.get_columns('Products')

    assert date['name'] == 'Date'
    assert isinstance(date['type'], Date)
    assert date['primary_key'] == 1

    assert sku['name'] == 'SKU'
    assert isinstance(sku['type'], Integer)
    assert sku['primary_key'] == 2

    assert price['name'] == 'Price'
    assert isinstance(sku['type'], Integer)
    assert not price['nullable']
