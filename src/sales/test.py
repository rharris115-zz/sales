from datetime import date
from io import StringIO

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from . import import_data, query, schema
from .query import SalesQuery


def test_query_average_sale_for_and_sku_price_by_sku_1241(session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_average_sold_for_and_sku_price_by_sku() \
        .with_skus(1241) \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert 1241 in result


def test_query_average_sale_for_and_sku_price_by_sku(session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_average_sold_for_and_sku_price_by_sku() \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert result


def test_query_average_sales_for_and_sku_price_by_staff_id_33(
        session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_average_sold_for_and_sku_price_by_staff_id() \
        .with_staff_ids(33) \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert 33 in result


def test_average_sales_for_and_sku_price_by_staff_id(session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_average_sold_for_and_sku_price_by_staff_id() \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert result


def test_query_sales_by_store_name_Cambridge(session_with_products_and_stores_and_sales_imported: Session):
    result = query.sales_by_store_name('Cambridge', session=session_with_products_and_stores_and_sales_imported)
    assert 'Cambridge' in result


def test_query_sales_by_store_name(session_with_products_and_stores_and_sales_imported: Session):
    result = query.sales_by_store_name(session=session_with_products_and_stores_and_sales_imported)
    assert result


def test_query_sales_by_sku_1241(session_with_products_and_stores_and_sales_imported: Session):
    result = query.sales_by_sku(1241, session=session_with_products_and_stores_and_sales_imported)
    assert 1241 in result


def test_query_sales_by_sku(session_with_products_and_stores_and_sales_imported: Session):
    result = query.sales_by_sku(session=session_with_products_and_stores_and_sales_imported)
    assert result


def test_query_sales_by_staff_id_33(session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_total_sales_by_staff() \
        .with_staff_ids(33) \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert 33 in result


def test_query_sales_by_staff_id(session_with_products_and_stores_and_sales_imported: Session):
    result = SalesQuery \
        .of_total_sales_by_staff() \
        .run(session=session_with_products_and_stores_and_sales_imported)
    assert result


def test_query_cambridgeshire(session_with_products_and_stores_and_sales_imported: Session):
    result = query.total_sales_by_postcode(session=session_with_products_and_stores_and_sales_imported,
                                           postcode_prefix='CB')
    assert 'CB1 2BT' in result
    assert result['CB1 2BT'] == 971.78


def test_import_sales_data_two(sales_two_data_csv: str,
                               sales_date: date,
                               session_with_products_and_stores_imported: Session):
    import_data.import_sales_data_from_source_two(business_date=sales_date,
                                                  sales_csv=StringIO(sales_two_data_csv),
                                                  session=session_with_products_and_stores_imported)
    imported_sales = session_with_products_and_stores_imported.query(schema.Sale).all()
    assert imported_sales


def test_import_sales_data_one(sales_one_data_json: str,
                               sales_date: date,
                               session_with_products_and_stores_imported: Session):
    import_data.import_sales_data_from_source_one(business_date=sales_date, sales_json=StringIO(sales_one_data_json),
                                                  session=session_with_products_and_stores_imported)
    imported_sales = session_with_products_and_stores_imported.query(schema.Sale).all()
    assert imported_sales


def test_update_good_store_data(good_store_json_data: str, session: Session):
    import_data.update_stores(stores=StringIO(good_store_json_data), session=session)
    stores = session.query(import_data.Store).all()
    assert stores


def test_import_good_product_data(sales_date: date, good_product_json_data: str, session: Session):
    import_data.import_products(date=sales_date, products=StringIO(good_product_json_data), session=session)
    imported_products = session.query(schema.Product).all()
    assert imported_products
    for p in imported_products:
        assert p.date == sales_date


def test_create_sales(engine_with_tables: Engine):
    instrument = inspect(subject=engine_with_tables)

    assert 'Sales' in instrument.get_table_names()

    [id, sku, business_date, sold_for, staff_id, timestamp, store_id] = instrument.get_columns('Sales')

    assert id['name'] == 'Id'
    assert id['primary_key'] == 1

    assert sku['name'] == 'SKU'
    assert not sku['nullable']

    assert business_date['name'] == 'BusinessDate'
    assert not business_date['nullable']

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
