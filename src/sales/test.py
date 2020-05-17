from io import StringIO

from sqlalchemy import inspect, Date, Integer, DateTime, String, Text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from . import data


def test_update_good_store_data(good_store_json_data: str, session: Session):
    data.update_stores(stores=StringIO(good_store_json_data), session=session)

    for s in session.query(data.Store):
        assert s.id is not None and isinstance(s.id, int)
        assert s.name is not None and isinstance(s.name, str)
        assert s.postcode is not None and isinstance(s.postcode, str)
        assert s.address is not None and isinstance(s.address, str)


def test_import_good_product_data(sales_date: data, good_product_json_data: str, session: Session):
    data.import_products(date=sales_date, products=StringIO(good_product_json_data), session=session)

    for p in session.query(data.Product):
        assert p.date == sales_date
        assert isinstance(p.sku, int)
        assert isinstance(p.price, int)


def test_create_sales(engine_with_tables: Engine):
    instrument = inspect(subject=engine_with_tables)

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


def test_create_stores(engine_with_tables: Engine):
    instrument = inspect(engine_with_tables)

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


def test_create_products(engine_with_tables: Engine):
    instrument = inspect(engine_with_tables)

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
