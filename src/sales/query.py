from typing import Dict

from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from .schema import Store, Sale, Product


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


def average_sales_for_and_sku_price_by_staff_id(*staff_ids, session: Session):
    q: Query = session.query(Sale.staff_id, func.count(), func.sum(Sale.sold_for),
                             func.sum(Product.price)) \
        .filter(Sale.business_date == Product.date) \
        .filter(Sale.sku == Product.sku)
    if staff_ids:
        q = q.filter(Sale.staff_id.in_(staff_ids))
    return {
        staff_id: (int(count), float(total_sold_for / count), float(total_sku_price / count))
        for staff_id, count, total_sold_for, total_sku_price in q.group_by(Sale.staff_id)
    }
