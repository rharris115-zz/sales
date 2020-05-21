from datetime import date
from typing import Tuple, Union

from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from .schema import Store, Sale, Product


class SalesQuery():

    def __init__(self, *values, key):
        self._key = key
        self._values = values

        self._skus: Tuple[str] = tuple()
        self._staff_ids: Tuple[int] = tuple()
        self._store_names: Tuple[str] = tuple()
        self._postcode_pattern: Union[str, type(None)] = None
        self._start: date = date.min
        self._finish: date = date.max

    @classmethod
    def of_total_sales_by_postcode(cls):
        return cls(func.sum(Sale.sold_for), key=Store.postcode)

    @classmethod
    def of_total_sales_by_store_name(cls):
        return cls(func.sum(Sale.sold_for), key=Store.name)

    @classmethod
    def of_total_sales_by_staff_id(cls):
        return cls(func.sum(Sale.sold_for), key=Sale.staff_id)

    @classmethod
    def of_total_sales_by_sku(cls):
        return cls(func.sum(Sale.sold_for), key=Sale.sku)

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

    def with_postcode_pattern(self, pattern: str):
        self._postcode_pattern = pattern
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
        if self._postcode_pattern is not None:
            q = q.filter(Store.postcode.like(self._postcode_pattern))

        return {
            key: tuple(values)
            for key, *values in q.group_by(self._key)
        }
