import os
import json
import hashlib
import unittest
from io import TextIOWrapper
from typing import (
    Any,
    Hashable,
)


def hash_password(password: str) -> str:
    hash_obj: Hashable = hashlib.sha512()
    hash_obj.update(password.encode('utf-8'))
    return hash_obj.hexdigest()


def read_data(path: str) -> Any:
    db: TextIOWrapper = open(path)
    data: Any = json.load(db)
    db.close()
    return data


def fill_data(path: str, data: list[dict]) -> None:
    db: TextIOWrapper = open(path, 'w')
    json.dump(data, db)
    db.close()


class AbstractTestCase(unittest.TestCase):
    """
    Remove and create databases for tests.
    """
    def setUp(self) -> None:
        if not os.path.exists('tests/db/'):
            os.mkdir('tests/db/')

    def tearDown(self) -> None:
        db_paths: list[str] = [
            'tests/db/user_db.json',
            'tests/db/db.json',
        ]

        for path in db_paths:
            if os.path.exists(path):
                os.remove(path)

        os.rmdir('tests/db')
