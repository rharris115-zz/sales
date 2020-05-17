from pathlib import Path
import pytest
from os import PathLike


@pytest.fixture
def db_path(tmpdir: PathLike) -> PathLike:
    return Path(tmpdir) / 'sales.db'
