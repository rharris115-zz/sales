import json
from datetime import date
from typing import IO

from sqlalchemy.orm import Session

from .schema import Product, Store


def import_products(date: date, products: IO[str], session: Session):
    data = json.loads(s=products.read())
    instances = [Product(date=date, sku=item['Sku'], price=round(100 * item['Price'])) for item in data]
    session.add_all(instances=instances)
    session.commit()


def update_stores(stores: IO[str], session: Session):
    data = json.loads(s=stores.read())
    instances = [Store(id=item['Id'], name=item['Name'], postcode=item['Postcode'], address=item['Address'])
                 for item in data]
    list(map(session.merge, instances))
    session.commit()
