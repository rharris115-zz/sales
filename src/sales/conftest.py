from os import PathLike
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from json import dumps


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
