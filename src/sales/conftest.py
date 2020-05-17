from os import PathLike
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@pytest.fixture
def db_path(tmpdir: PathLike) -> PathLike:
    return Path(tmpdir) / 'sales.db'


@pytest.fixture
def engine(db_path: PathLike) -> Engine:
    path = 'sqlite:///' + str(db_path)
    return create_engine(path)
