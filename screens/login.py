from .screen import Screen
from . import menu


class LoginScreen(Screen):
    """
    Tela responsável por pegar os dados de autenticação do usuário
    e validar seu login.
    """
    def __init__(self) -> None:
        super().__init__()
        self.get_username()

    @property
    def screen_name(self) -> str:
        return f"{' Login ':=^70}"

    def get_username(self):
        msg = 'Aperte "enter" para ir para o menu de opções\n'
        msg += "ou digite seu nome de usuário para prosseguir.\n\n"
        msg += "username:"

        action: str = self.get_user_input(msg)
        match action:
            case "":
                return menu.MenuScreen()

            case _:
                self.get_username()

    def is_exiting(self):
        exiting: str = self.get_user_input(
            "Deseja sair do programa? [s/N]:"
        )
        if exiting == "s":
            exit()
        self.get_username()

    def render(self) -> None:
        super().render()
