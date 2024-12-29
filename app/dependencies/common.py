from typing import Callable
from tinydb import TinyDB

def db_connection(db_path: str) -> Callable[[], TinyDB]:
    def dependency() -> TinyDB:
        return TinyDB(db_path, indent=4)
    return dependency