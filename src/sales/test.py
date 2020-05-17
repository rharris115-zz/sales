import sqlite3
from os import PathLike
from . import data


def test_create_products_if_not_exists(db_path: PathLike):
    with sqlite3.connect(db_path) as conn:
        data.create_products_if_not_exists(conn=conn)
