import csv
import datetime
import json
from typing import IO, Dict

import pytz
from sqlalchemy.orm import Session

from .schema import Product, Store, Sale

_uk_time_zone = pytz.timezone('Europe/London')


def import_products(date: datetime.date, products: IO[str], session: Session):
    for item in json.loads(s=products.read()):
        # It seems this data source uses 'p' as a unit of price and this must be converted to '£'.
        session.add(Product(date=date, sku=item['Sku'], price=item['Price'] / 100))
    session.commit()


def update_stores(stores: IO[str], session: Session):
    for item in json.loads(s=stores.read()):
        store = Store(id=item['Id'], name=item['Name'], postcode=item['Postcode'], address=item['Address'])
        session.merge(store)

    session.commit()


def _sku_prices_on(sales_date: datetime.date, session: Session) -> Dict[int, float]:
    # Query the sku prices for the sales_date. This should already have been imported.
    price_by_sku = {sku: float(price)
                    for sku, price in session.query(Product.sku, Product.price).filter(Product.date == sales_date)}
    assert price_by_sku, f'No product data for date={sales_date}.'
    return price_by_sku


def import_sales_data_from_source_one(sales_date: datetime.date, sales_json: IO[str], session: Session):
    price_by_sku = _sku_prices_on(sales_date=sales_date, session=session)

    # Query the store names by id.
    store_id_by_name = {name: id for name, id in session.query(Store.name, Store.id)}

    record_ids = set()

    for sale_record in json.loads(s=sales_json.read()):

        # Its possible to have duplicate Sales records in this source on any day. We use the 'Id' field
        # to test for this so that subsequent records with a non-unique 'Id' are ignored.
        record_id = sale_record['Id']
        if record_id in record_ids:
            continue
        elif record_id is not None:
            record_ids.add(record_id)

        sku = sale_record['Sku']
        discount_percent = sale_record['DiscountPercent']
        staff_id = sale_record['StaffId']
        timestamp = pytz.utc.localize(datetime.datetime.strptime(sale_record['SoldAtUtc'], '%Y-%m-%dT%H:%M:%SZ'))
        store_name = sale_record['Store']

        assert timestamp.astimezone(_uk_time_zone).date() == sales_date, \
            f'sale_record({sale_record}) can only come from the specified UTC date({sales_date}).'

        sold_for = price_by_sku.get(sku) * (1 - float(discount_percent) / 100)
        store_id = store_id_by_name[store_name]

        sale = Sale(sku=sku, sold_for=sold_for, staff_id=staff_id, timestamp=timestamp, store_id=store_id)

        session.add(sale)

    session.commit()


def import_sales_data_from_source_two(sales_date: datetime.date, sales_csv: IO[str], session: Session):
    price_by_sku = _sku_prices_on(sales_date=sales_date, session=session)

    # Query the store names by id.
    store_ids = {id for (id,) in session.query(Store.id)}

    for row in csv.DictReader(sales_csv):
        sku = int(row['Sku'])
        sold_for = float(row['SoldFor'])
        staff_id = int(row['StaffId'])
        timestamp = pytz.utc.localize(datetime.datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M:%S'))
        store_id = int(row['StoreId'])
        discounted = row['Discounted'] == 'True'

        if timestamp.year == 1:
            timestamp = datetime.datetime.combine(sales_date, datetime.datetime.min.time())

        assert timestamp.astimezone(_uk_time_zone).date() == sales_date, \
            f'sale_record({row}) can only come from the specified UTC date({sales_date}).'

        assert sku in price_by_sku, f'No price data found for sku({sku}) on day({sales_date})'

        sku_price = price_by_sku[sku]

        # We effectively don't have a sold_for value for this sale and must infer from it's sku price.
        if sold_for == 0:
            assert not discounted, f'Can\'t infer sold_for from sku_price({sku_price}) if the sale is discounted.'
            sold_for = sku_price

        # Use the 'Discounted' field and the sku price to check for consistency.
        if discounted:
            assert sku_price > sold_for, f'Sale is discounted, but sku_price({sku_price}) <=  sold_for({sold_for})'
        else:
            assert sku_price == sold_for, f'Sale is not discounted, but sku_price({sku_price}) !=  sold_for({sold_for})'

        assert store_id in store_ids, f'store_id({store_id}) not known.'

        sale = Sale(sku=sku, sold_for=sold_for, staff_id=staff_id, timestamp=timestamp, store_id=store_id)
        session.add(sale)

    session.commit()
