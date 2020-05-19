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
