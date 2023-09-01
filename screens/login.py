from .screen import Screen
from .todo import ToDoListScreen
from .register import RegisterScreen


class LoginScreen(Screen):
    """
    Tela responsável por pegar os dados de autenticação do usuário
    e validar seu login.
    """
    def __init__(self) -> None:
        super().__init__()
        action: str = self.get_action()

        if action == '':
            self.register
        else:
            self.login(action)

    @property
    def register(self) -> RegisterScreen:
        return RegisterScreen()

    @property
    def screen_name(self) -> str:
        return f"{' Login ':=^50}"

    def login(self, username: str) -> ToDoListScreen:
        password: str = self.get_user_input(
            "senha:",
            password=True,
            render_kwargs={"username": username}
        )
        del password
        # TODO
        return ToDoListScreen()

    def get_action(self) -> str:
        action: str = self.get_user_input("usuário:")
        return action

    def render(
        self,
        info: bool = True,
        username: str = ""
    ) -> None:
        super().render()

        if username == "":
            print("Para criar uma nova conta, aperte enter")
        else:
            print(f"Bem vindo(a) de volta, {username.capitalize()}")
