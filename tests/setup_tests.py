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
        path: str = 'tests/db/user_db.json'

        if os.path.exists(path):
            os.remove(path)

        os.rmdir('tests/db')
