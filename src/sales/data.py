import csv
import datetime
import json
from typing import IO, Dict, Any

import pytz
from sqlalchemy.orm import Session

from .schema import Product, Store, Sale

uk_time_zone = pytz.timezone('Europe/London')


def import_products(date: datetime.date, products: IO[str], session: Session):
    data = json.loads(s=products.read())
    instances = [Product(date=date, sku=item['Sku'], price=item['Price'])
                 for item in data]
    session.add_all(instances=instances)
    session.commit()


def update_stores(stores: IO[str], session: Session):
    data = json.loads(s=stores.read())

    for item in data:
        store = Store(id=item['Id'], name=item['Name'], postcode=item['Postcode'], address=item['Address'])
        session.merge(store)

    session.commit()


def import_sales_data_from_source_one(sales_date: datetime.date, sales_json: IO[str], session: Session):
    # Query the sku prices for the day of this sales data. This should already have been imported.
    price_by_sku = {sku: float(price)
                    for sku, price in session.query(Product.sku, Product.price).filter(Product.date == sales_date)}
    assert price_by_sku, f'No price by SKU data for date={sales_date}.'

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

        assert timestamp.astimezone(uk_time_zone).date() == sales_date, \
            f'sale_record({sale_record}) can only come from the specified UTC date({sales_date}).'

        sold_for = price_by_sku.get(sku) * (1 - float(discount_percent) / 100)
        store_id = store_id_by_name[store_name]

        sale = Sale(sku=sku, sold_for=sold_for, staff_id=staff_id, timestamp=timestamp, store_id=store_id)

        session.add(sale)

    session.commit()


def import_sales_data_from_source_two(sales_date: datetime.date, sales_csv: IO[str], session: Session):
    # Query the sku prices for the day of this sales data. This should already have been imported.
    price_by_sku = {sku: float(price)
                    for sku, price in session.query(Product.sku, Product.price).filter(Product.date == sales_date)}
    assert price_by_sku, f'No price by SKU data for date={sales_date}.'

    # Query the store names by id.
    store_ids = {id for (id,) in session.query(Store.id)}

    for row in csv.DictReader(sales_csv):
        sku = int(row['Sku'])
        sold_for = float(row['SoldFor'])
        staff_id = int(row['StaffId'])
        timestamp = pytz.utc.localize(datetime.datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M:%S'))
        store_id = int(row['StoreId'])
        discounted = bool(row['Discounted'])

        if timestamp.year == 1:
            timestamp = datetime.datetime.combine(sales_date, datetime.datetime.min.time())

        assert timestamp.astimezone(uk_time_zone).date() == sales_date, \
            f'sale_record({row}) can only come from the specified UTC date({sales_date}).'

        assert sku in price_by_sku, f'No price data found for sku({sku}) on day({sales_date})'

        # Use the 'Discounted' field and the sku price to check for consistency.
        sku_price = price_by_sku[sku]
        if discounted:
            assert sku_price > sold_for, f'Sale is discounted, but sku_price({sku_price}) <=  sold_for({sold_for})'
        else:
            assert sku_price == sold_for, f'Sale is not discounted, but sku_price({sku_price}) !=  sold_for({sold_for})'

        assert store_id in store_ids, f'store_id({store_id}) not known.'

        sale = Sale(sku=sku, sold_for=sold_for, staff_id=staff_id, timestamp=timestamp, store_id=store_id)
        session.add(sale)

    session.commit()
