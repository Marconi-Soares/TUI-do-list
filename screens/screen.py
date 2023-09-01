import os
from getpass import getpass
from assets.utils import LOGO


class Screen:
    def __init__(self) -> None:
        self.render()

    def __str__(self) -> str:
        return 'Screen'

    def get_user_input(
        self, msg: str,
        password: bool = False,
        render_kwargs: dict = {}
    ) -> str:
        """
        Get user input and then call render to refresh the TUI
        """
        user_input: str
        msg += "\n>>> "

        self.render(**render_kwargs)

        if password:
            user_input = getpass(msg)
        else:
            user_input = input(msg)

        return user_input

    @property
    def screen_name(self):
        raise NotImplementedError

    def render(self) -> None:
        os.system("clear")
        print(LOGO)
        print(self.screen_name)
