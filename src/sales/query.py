from typing import Dict, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from .schema import Store, Sale, Product
from datetime import date


def total_sales_by_postcode(session: Session, postcode_prefix: str = '') -> Dict[str, float]:
    return {
        postcode: float(total)
        for postcode, total in session
            .query(Store.postcode, func.sum(Sale.sold_for))
            .filter(Store.id == Sale.store_id)
            .filter(Store.postcode.startswith(postcode_prefix))
            .group_by(Store.postcode)
    }


def sales_by_sku(*skus, session: Session) -> Dict[int, float]:
    q: Query = session.query(Sale.sku, func.sum(Sale.sold_for))
    if skus:
        q = q.filter(Sale.sku.in_(skus))
    return {
        sku: float(total)
        for sku, total in q.group_by(Sale.sku)
    }


def sales_by_store_name(*store_names, session: Session) -> Dict[str, float]:
    q: Query = session.query(Store.name, func.sum(Sale.sold_for)) \
        .filter(Store.id == Sale.store_id)
    if store_names:
        q = q.filter(Store.name.in_(store_names))
    return {
        store_name: float(total)
        for store_name, total in q.group_by(Store.name)
    }


class SalesQuery():

    def __init__(self, *values, key):
        self._key = key
        self._values = values

        self._skus: Tuple[str] = tuple()
        self._staff_ids: Tuple[int] = tuple()
        self._store_names: Tuple[str] = tuple()

        self._start: date = date.min
        self._finish: date = date.max

    @classmethod
    def of_total_sales_by_staff(cls):
        return cls(func.sum(Sale.sold_for), key=Sale.staff_id)

    @classmethod
    def of_average_sold_for_and_sku_price_by_staff_id(cls):
        return cls(func.count(), func.avg(Sale.sold_for), func.avg(Product.price), key=Sale.staff_id)

    @classmethod
    def of_average_sold_for_and_sku_price_by_sku(cls):
        return cls(func.count(), func.avg(Sale.sold_for), Product.price, key=Sale.sku)

    @classmethod
    def of_average_sold_for_and_sku_price_by_store_name(cls):
        return cls(func.count(), func.avg(Sale.sold_for), func.avg(Product.price), key=Store.name)

    def with_skus(self, *skus):
        self._skus = skus
        return self

    def with_staff_ids(self, *staff_ids):
        self._staff_ids = staff_ids
        return self

    def with_store_names(self, *store_names):
        self._store_names = store_names
        return self

    def starting(self, date: date):
        self._start = date
        return self

    def finishing(self, date: date):
        self._finish = date
        return self

    def run(self, session: Session):
        q: Query = session.query(self._key, *self._values) \
            .filter(Sale.business_date == Product.date) \
            .filter(Sale.sku == Product.sku) \
            .filter(Store.id == Sale.store_id)

        if self._skus:
            q = q.filter(Sale.sku.in_(self._skus))
        if self._staff_ids:
            q = q.filter(Sale.staff_id.in_(self._staff_ids))
        if self._store_names:
            q = q.filter(Store.name.in_(self._store_names))
        if self._start > date.min:
            q = q.filter(Sale.business_date >= self._start)
        if self._finish < date.max:
            q = q.filter(Sale.business_date <= self._finish)

        return {
            key: values
            for key, *values in q.group_by(self._key)
        }
