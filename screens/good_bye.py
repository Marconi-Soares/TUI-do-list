import os
from .screen import Screen
from assets.utils import ADEUS


class GoodByeScreen(Screen):
    def __init__(self):
        super().__init__()

    @property
    def screen_name(self):
        return f"{' Adeus ':=^50}"

    def render(self):
        os.system('clear')
        print(ADEUS)
        exit()
