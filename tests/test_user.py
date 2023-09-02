import os
import unittest
from db.users.user import User
from db.users.user_list import UserList


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir('tests/db/')

    def tearDown(self) -> None:
        os.remove('tests/db/user_db.json')
        os.rmdir('tests/db/')

    def test_user_create_success(self):
        user = User(username='marconi', password='123')
        user.DB_PATH = 'my_db.json'
        users = UserList()
        users.DB_PATH = 'my_db.json'
        users.append(user)

