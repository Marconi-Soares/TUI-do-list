from .register import RegisterScreen
from .good_bye import GoodByeScreen
from .screen import Screen


class MenuScreen(Screen):
    def __init__(self):
        super().__init__()
        self.get_action()

    @property
    def screen_name(self) -> str:
        return f"{' Menu ':=^70}"

    def get_action(self):
        msg = "[1] Novo Usuário\n"
        msg += "[2] Sair\n"
        msg += "[3] Informações"

        action: str = self.get_user_input(msg)

        match action:
            case "1":
                RegisterScreen()

            case "2":
                GoodByeScreen()

            case "3":
                exit()

    def render(self) -> None:
        super().render()
