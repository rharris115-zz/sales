from . import data
from sqlalchemy import inspect


def test_create_products_if_not_exists(engine):
    data.create_products_if_not_exists(engine=engine)
    assert 'Products' in inspect(engine).get_table_names()
