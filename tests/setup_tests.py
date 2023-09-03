import os
import unittest


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
