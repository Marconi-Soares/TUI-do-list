from . import login
from .screen import Screen
from .good_bye import GoodByeScreen
from db.users.user import User
from db.users.user_list import UserList
from components.warnings import Warnings


class RegisterScreen(Screen):
    def __init__(self):
        super().__init__()
        username: str = self.get_username()
        password: str = self.get_password()

        user: User = User(username=username, password=password)
        UserList.append(user)

    @property
    def screen_name(self) -> str:
        return f"{' Registro de Usuário ':=^70}"

    def perform_action(self, action):
        match action:
            case '!voltar':
                return login.LoginScreen()

            case '!sair':
                return GoodByeScreen()

    def get_input_message(
        self,
        field: str,
        prefix: str,
        value: str,
        errors: list[str]
    ) -> str:

        if value == "":
            errors.append(f'{prefix} não poder ser vazio.')

        if len(value) <= 5:
            errors.append(f'{prefix} deve conter ao menos de 5 letras.')

        if ' ' in value:
            errors.append(
                f'{prefix} deve conter apenas letras, números e simbolos.'
            )

        warnings: Warnings = Warnings(errors)

        input_message: str = str(warnings)
        input_message += f'\n{field}:'

        return input_message

    def get_username(self):
        username: str = ""
        errors: list[str] = []

        while True:
            msg: str = self.get_input_message(
                'username',
                'O nome de usuário',
                username,
                errors
            )

            if len(errors) > 0:
                username = self.get_user_input(msg)
                errors = []
                continue

            try:
                UserList().get('username', username)
                errors.append(f'"{username}" já está sendo usado.')
                continue
            except StopIteration:
                break

        return username

    def get_password(self, errors: list[str] = []) -> str:
        if len(errors) > 0:
            password: str = 'dontRaiseErr'
        else:
            password: str = ''

        while True:
            msg: str = self.get_input_message(
                'senha',
                'A senha',
                password,
                errors
            )

            if len(errors) > 0:
                password = self.get_user_input(msg, password=True)
                errors = []
                continue
            break

        password2: str = self.get_user_input(
            'Confirme a senha:',
            password=True
        )

        if not password == password2:
            return self.get_password(['As senhas não coincidem'])

        return password

    def render(self):
        super().render()
        print(" [!sair]   -> para fechar o programa")
        print(" [!voltar] -> para voltar a tela de login")
        print('*'*70)
