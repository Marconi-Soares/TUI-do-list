import os
from db.users.user import UserDict, User
from db.users.user_list import UserList
from .setup_tests import (
    fill_data,
    read_data,
    AbstractTestCase,
)


class TestUserList(AbstractTestCase):
    PATH: str = 'tests/db/user_db.json'

    def test_user_list_is_fetching_db_data(self):
        """
        Os dados da lista de usuários de usuários são
        pegos no banco de dados. Essa ação deve criar um
        novo arquivo de banco de dados caso não haja.
        """
        self.assertFalse(os.path.exists(self.PATH))
        UserList().all()
        self.assertTrue(os.path.exists(self.PATH))

    def test_user_list_len_method_return_the_number_of_users(self):
        self.assertEqual(len(UserList()), 0)
        user_dict: UserDict = {
            'id': '123',
            'username': 'Test',
            'password': '123'
        }
        fill_data(self.PATH, [user_dict])
        self.assertEqual(len(UserList()), 1)

    def test_append_user_without_db_created(self):
        user: User = User(username='marconi', password='123')
        user_dict: UserDict = {
            **user.to_dict,
            'password': user.password
        }
        UserList.append(user)

        saved_user: list[dict] = read_data(self.PATH)
        self.assertListEqual(saved_user, [user_dict])

    def test_append_user_with_previous_data(self):
        user_dict: UserDict = {
                "id": '123',
                "username": 'Test',
                'password': '123'
        }
        fill_data(self.PATH, [user_dict])

        user: User = User(username='marconi', password='123')
        UserList.append(user)
        saved_users: list[dict] = read_data(self.PATH)
        self.assertDictEqual(saved_users[0], user_dict)

    def test_cant_save_non_saveble_users(self):
        user: User = User(id='123', username='123')
        with self.assertRaises(ValueError):
            UserList.append(user)
