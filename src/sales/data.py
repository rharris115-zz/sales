import datetime
import json
from typing import IO

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
    instances = [
        Store(id=item['Id'], name=item['Name'], postcode=item['Postcode'], address=item['Address'])
        for item in data
    ]
    list(map(session.merge, instances))
    session.commit()


def import_sales_data_from_source_one(sales_json: IO[str], session: Session):
    data = json.loads(s=sales_json.read())

    def _as_utc_timezone(timestamp: str) -> datetime.datetime:
        return pytz.utc.localize(datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ'))

    # Infer the date from the sales data timestamps.

    # Data seems to be reported in a day that starts at 2300 UTC during daylight savings time. This is likely due to
    # daylight savings in the UK timezone. Before reporting the date of a timestamp, we should first convert it to local
    # UK time.
    days = {_as_utc_timezone(item['SoldAtUtc']).astimezone(tz=uk_time_zone).date() for item in data}
    assert len(days) == 1, f'There should only be one day represented in the sales data. days={days}'
    date = next(iter(days))

    # Query the sku prices for the day of this sales data. This should already have been imported.
    price_by_sku = {sku: float(price)
                    for sku, price in session.query(Product.sku, Product.price).filter(Product.date == date)}
    assert price_by_sku, 'No price by SKU data.'

    # Query the store names by id.
    store_id_by_name = {name: id for name, id in session.query(Store.name, Store.id)}

    record_ids = set()

    for item in data:

        # Its possible to have duplicate Sales records in this source on the day. We use the 'Id' field
        # to test for this so that subsequent records with a non-unique 'Id' are ignored.
        record_id = item['Id']
        if record_id in record_ids:
            continue
        elif record_id is not None:
            record_ids.add(record_id)

        sku = item['Sku']
        discount_percent = item['DiscountPercent']
        staff_id = item['StaffId']
        timestamp = _as_utc_timezone(item['SoldAtUtc'])
        store_name = item['Store']

        sold_for = price_by_sku.get(sku) * (1 - float(discount_percent) / 100)
        store_id = store_id_by_name[store_name]

        sale = Sale(sku=sku, sold_for=sold_for, staff_id=staff_id, timestamp=timestamp, store_id=store_id)

        session.add(sale)

    session.commit()
