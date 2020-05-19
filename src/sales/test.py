from datetime import date
from io import StringIO

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from . import data, schema


def test_import_sales_data_two(sales_two_data_csv: str,
                               good_store_json_data: str,
                               sales_date: date,
                               good_product_json_data: str,
                               session: Session):
    # In order to test the import of sales data, we first need to populate the db with store and product
    # data.
    data.update_stores(stores=StringIO(good_store_json_data), session=session)
    data.import_products(date=sales_date, products=StringIO(good_product_json_data), session=session)

    data.import_sales_data_from_source_two(sales_json=StringIO(sales_two_data_csv), session=session)

    imported_sales = session.query(schema.Sale).all()

    assert imported_sales


def test_import_sales_data_one(sales_one_data_json: str,
                               good_store_json_data: str,
                               sales_date: date,
                               good_product_json_data: str,
                               session: Session):
    # In order to test the import of sales data, we first need to populate the db with store and product
    # data.
    data.update_stores(stores=StringIO(good_store_json_data), session=session)
    data.import_products(date=sales_date, products=StringIO(good_product_json_data), session=session)

    data.import_sales_data_from_source_one(sales_json=StringIO(sales_one_data_json), session=session)

    imported_sales = session.query(schema.Sale).all()

    assert imported_sales


def test_update_good_store_data(good_store_json_data: str, session: Session):
    data.update_stores(stores=StringIO(good_store_json_data), session=session)

    assert session.query(data.Store).all()


def test_import_good_product_data(sales_date: date, good_product_json_data: str, session: Session):
    data.import_products(date=sales_date, products=StringIO(good_product_json_data), session=session)

    imported_products = session.query(schema.Product).all()

    for p in imported_products:
        assert p.date == sales_date


def test_create_sales(engine_with_tables: Engine):
    instrument = inspect(subject=engine_with_tables)

    assert 'Sales' in instrument.get_table_names()

    [id, sku, sold_for, staff_id, timestamp, store_id] = instrument.get_columns('Sales')

    assert id['name'] == 'Id'
    assert id['primary_key'] == 1

    assert sku['name'] == 'SKU'
    assert not sku['nullable']

    assert sold_for['name'] == 'SoldFor'
    assert not sold_for['nullable']

    assert staff_id['name'] == 'StaffId'
    assert not staff_id['nullable']

    assert timestamp['name'] == 'Timestamp'

    assert store_id['name'] == 'StoreId'
    assert not store_id['nullable']


def test_create_stores(engine_with_tables: Engine):
    instrument = inspect(engine_with_tables)

    assert 'Stores' in instrument.get_table_names()

    [id, name, postcode, address] = instrument.get_columns('Stores')

    assert id['name'] == 'Id'
    assert id['primary_key'] == 1

    assert name['name'] == 'Name'
    assert name['type'].length == 40
    assert not name['nullable']

    assert postcode['name'] == 'Postcode'
    assert postcode['type'].length == 8
    assert not postcode['nullable']

    assert address['name'] == 'Address'
    assert not address['nullable']


def test_create_products(engine_with_tables: Engine):
    instrument = inspect(engine_with_tables)

    assert 'Products' in instrument.get_table_names()

    [date, sku, price] = instrument.get_columns('Products')

    assert date['name'] == 'Date'
    assert date['primary_key'] == 1

    assert sku['name'] == 'SKU'
    assert sku['primary_key'] == 2

    assert price['name'] == 'Price'
    assert not price['nullable']
