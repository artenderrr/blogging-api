from typing import Generator
import pytest
from tests.utils import Backup, FileManager

@pytest.fixture(scope="session", autouse=True)
def backup() -> Generator[None, None, None]:
    backup = Backup(source_dir="app/db", backup_dir="tests/backup")
    yield
    backup.restore()

@pytest.fixture(autouse=True)
def cleanup() -> None:
    FileManager.clear_directory("app/db")