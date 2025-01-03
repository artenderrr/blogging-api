from typing import Generator
import pytest
from pytest import FixtureRequest
from tests.utils import Backup, FileManager, AuthorizationData

@pytest.fixture(scope="session", autouse=True)
def backup() -> Generator[None, None, None]:
    backup = Backup(source_dir="app/db", backup_dir="tests/backup")
    yield
    backup.restore()

@pytest.fixture(autouse=True)
def cleanup() -> None:
    FileManager.clear_directory("app/db")

@pytest.fixture
def authorization(request: FixtureRequest) -> AuthorizationData:
    credentials = getattr(request, "param", None)
    return AuthorizationData(credentials=credentials)