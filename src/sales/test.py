from . import data
from sqlalchemy import inspect


def test_create_products(engine):
    data.create_tables(engine=engine)
    assert 'Products' in inspect(engine).get_table_names()
