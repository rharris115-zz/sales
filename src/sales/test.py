from . import data
from sqlalchemy import inspect, Date, Integer
from sqlalchemy.engine import Engine


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
