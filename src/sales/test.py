from . import data
from sqlalchemy import inspect, Date, Integer, String, Text
from sqlalchemy.engine import Engine


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
    assert name['primary_key'] == 2

    assert postcode['name'] == 'Postcode'
    assert isinstance(postcode['type'], String)
    assert not postcode['nullable']

    assert address['name'] == 'Postcode'
    assert isinstance(address['type'], String)
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
