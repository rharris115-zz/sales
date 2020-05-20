from typing import Dict

from sqlalchemy import func
from sqlalchemy.orm import Session

from .schema import Store, Sale


def total_sales_by_postcode(session: Session, postcode_prefix: str = '') -> Dict[str, float]:
    return {
        postcode: float(total)
        for postcode, total in session \
            .query(Store.postcode, func.sum(Sale.sold_for)) \
            .join(Store) \
            .filter(Store.postcode.startswith(postcode_prefix)) \
            .group_by(Store.postcode) \
        }


def total_sales_by_staff_id(session: Session) -> Dict[int, float]:
    return {
        staff_id: float(total)
        for staff_id, total in session \
            .query(Sale.staff_id, func.sum(Sale.sold_for))
            .group_by(Sale.staff_id)
    }
