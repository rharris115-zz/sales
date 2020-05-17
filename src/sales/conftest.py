from datetime import date
from json import dumps
from os import PathLike
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from . import data


@pytest.fixture
def db_path(tmpdir: PathLike) -> PathLike:
    return Path(tmpdir) / 'sales.db'


@pytest.fixture
def engine(db_path: PathLike) -> Engine:
    path = 'sqlite:///' + str(db_path)
    return create_engine(path)


@pytest.fixture
def good_product_json_data() -> str:
    return dumps([
        {
            "Sku": 1241,
            "Price": 1099.0
        },
        {
            "Sku": 4325,
            "Price": 3999.0
        },
        {
            "Sku": 1546,
            "Price": 10999.0
        },
        {
            "Sku": 7653,
            "Price": 1099.0
        },
        {
            "Sku": 2536,
            "Price": 5929.0
        },
        {
            "Sku": 5345,
            "Price": 9998.0
        }
    ])


@pytest.fixture
def good_store_json_data() -> str:
    return dumps([
        {
            "Id": 1,
            "Name": "Cambridge",
            "Postcode": "CB1 2BT",
            "Address": "1 High Street, Cambridge,CB1 2BT"
        },
        {
            "Id": 2,
            "Name": "Peterborough",
            "Postcode": "PE1 4HG",
            "Address": "1 High Street, Peterborough,PE1 4HG"
        },
        {
            "Id": 3,
            "Name": "St Ives",
            "Postcode": "PE27 3AB",
            "Address": "1 High Street, St Ives,PE27 3AB"
        },
        {
            "Id": 4,
            "Name": "Stevenage",
            "Postcode": "SG2 6BG",
            "Address": "1 High Street, Stevenage,SG2 6BG"
        },
        {
            "Id": 5,
            "Name": "Royston",
            "Postcode": "SG8 5RY",
            "Address": "1 High Street, Royston,SG8 5RY"
        },
        {
            "Id": 6,
            "Name": "Bury St Edmunds",
            "Postcode": "IP32 6AD",
            "Address": "1 High Street, Bury St Edmunds,IP32 6AD"
        },
        {
            "Id": 7,
            "Name": "Norwich",
            "Postcode": "NR1 5BT",
            "Address": "1 High Street, Norwich,NR1 5BT"
        },
        {
            "Id": 8,
            "Name": "Chelmsford",
            "Postcode": "CM3 8TU",
            "Address": "1 High Street, Chelmsford,CM3 8TU"
        }
    ])


@pytest.fixture
def sales_date() -> date:
    return date(2020, 5, 14)


@pytest.fixture
def engine_with_tables(engine: Engine):
    data.create_tables(engine=engine)
    return engine


@pytest.fixture
def session(engine_with_tables: Engine) -> Session:
    return sessionmaker(bind=engine_with_tables)()
