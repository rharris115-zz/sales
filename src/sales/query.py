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


def total_sales_by_staff_id(*staff_ids, session: Session) -> Dict[int, float]:
    q: Query = session.query(Sale.staff_id, func.sum(Sale.sold_for))
    if staff_ids:
        q = q.filter(Sale.staff_id.in_(staff_ids))
    return {
        staff_id: float(total)
        for staff_id, total in q.group_by(Sale.staff_id)
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


class SalesQueryBuilder():

    def __init__(self, key, sold_for, sku_price):
        self._key = key
        self._sold_for = sold_for
        self._sku_price = sku_price

        self._skus: Tuple[str] = tuple()
        self._staff_ids: Tuple[int] = tuple()
        self._store_names: Tuple[str] = tuple()

        self._start: date = date.min
        self._finish: date = date.max

    @classmethod
    def by_staff_id(cls):
        return cls(key=Sale.staff_id, sold_for=func.avg(Sale.sold_for), sku_price=func.avg(Product.price))

    @classmethod
    def by_sku(cls):
        return cls(key=Sale.sku, sold_for=func.avg(Sale.sold_for), sku_price=Product.price)

    @classmethod
    def by_store_name(cls):
        return cls(key=Store.name, sold_for=func.avg(Sale.sold_for), sku_price=func.avg(Product.price))

    def of_skus(self, *skus):
        self._skus = skus
        return self

    def of_staff_ids(self, *staff_ids):
        self._staff_ids = staff_ids
        return self

    def of_store_names(self, *store_names):
        self._store_names = store_names
        return self

    def starting(self, date: date):
        self._start = date
        return self

    def finishing(self, date: date):
        self._finish = date
        return self

    def run(self, session: Session):
        q: Query = session.query(self._key, func.count(), self._sold_for, self._sku_price) \
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
            q = q.filter(Sale.business_date > self._start)
        if self._finish < date.max:
            q = q.filter(Sale.business_date < self._finish)

        return {
            key: (int(count), float(sold_for), float(sku_price))
            for key, count, sold_for, sku_price in q.group_by(self._key)
        }
