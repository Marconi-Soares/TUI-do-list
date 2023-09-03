from .setup_tests import hash_password
from .setup_tests import AbstractTestCase
from db.users.user import (
    User,
    UserSerializationDict
)


class TestUser(AbstractTestCase):
    def test_user_id_is_created_when_not_provided(self) -> None:
        """
        Se um usuário for instanciado sem um id, deve gerar um
        uuid4.
        """
        user: User = User()
        self.assertIsNotNone(user.id)

    def test_user_id_is_not_created_when_provided(self) -> None:
        """
        Se um id for usado para instanciar um usuário, o usuário
        não deve gerar um novo id.
        """
        user: User = User(id='123')
        self.assertEqual(user.id, '123')

    def test_user_password_is_not_hashed_when_not_provided(self) -> None:
        """
        Se um usuário for instanciado sem uma senha, então não deve
        ser gerado um hash para essa senha.
        """
        user: User = User()
        self.assertIsNone(user.password)

    def test_user_password_is_hashed_when_provided(self) -> None:
        """
        Se um usuário for instanciado usando uma senha, então deve
        ser gerado um hash para essa senha.
        OBS: hash512 resulta em 128 chars.
        """
        user: User = User(password='senha')
        self.assertNotEqual(user.password, 'senha')
        self.assertEqual(len(str(user.password)), 128)

    def test_user_password_hash_is_acheaveble(self) -> None:
        """
        Ao digitar a mesma senha, o hash dessa senha deve
        ser igual ao hash salvo no banco de dados.
        """
        password: str = 'senha'
        user: User = User(password=password)
        self.assertEqual(user.password, hash_password(password))

    def test_user_can_be_instanciated_with_all_fields(self) -> None:
        """
        Um usuário pode ser instanciado com todos os campos
        para fins de serialização. A senha será modificada e
        não haverá nenhuma validação do nome de usuário.
        """
        user: User = User(password='senha', username='username', id='123')
        self.assertEqual(user.id, '123')
        self.assertEqual(user.username, 'username')
        self.assertNotEqual(user.password, 'senha')

    def test_user_without_password_is_not_saveble(self) -> None:
        """
        Um usuário que foi instanciado sem sua senha não pode
        ser salvo no banco de dados.
        """
        user: User = User(username='username')
        self.assertFalse(user.is_saveble)

    def test_user_without_username_is_not_saveble(self) -> None:
        """
        Um usuário que foi instanciado sem seu nome de usuário
        não pode ser salvo no bando de dados.
        """
        user: User = User(password='senha')
        self.assertFalse(user.is_saveble)

    def test_user_deserialization_with_all_fields(self) -> None:
        """
        Uma instancia de User pode ser serializada através do método
        to_dict que retornará apenas o id e o username.
        """
        user: User = User(
            username='Harry Potter',
            id='42',
            password='mal feito feito'
        )
        serialized_user: UserSerializationDict = user.to_dict
        self.assertIsNone(serialized_user.get('password'))
        self.assertEqual(serialized_user.get('id'), user.id)
        self.assertEqual(serialized_user.get('username'), user.username)

    def test_user_deserialization_with_username_and_password(self) -> None:
        user: User = User(username='Harry Potter', password='mal feito feito')
        serialized_user: UserSerializationDict = user.to_dict
        self.assertIsNone(serialized_user.get('password'))
        self.assertEqual(serialized_user.get('id'), user.id)
        self.assertEqual(serialized_user.get('username'), user.username)

    def test_user_deserialization_with_username_only(self) -> None:
        user: User = User(username='Harry Potter')
        serialized_user: UserSerializationDict = user.to_dict
        self.assertIsNone(serialized_user.get('password'))
        self.assertEqual(serialized_user.get('id'), user.id)
        self.assertEqual(serialized_user.get('username'), user.username)

    def test_user_deserialization_without_any_field(self) -> None:
        user: User = User()
        serialized_user: UserSerializationDict = user.to_dict
        self.assertIsNone(serialized_user.get('password'))
        self.assertEqual(serialized_user.get('id'), user.id)
        self.assertEqual(serialized_user.get('username'), user.username)
