import os
from screens import login


if __name__ == "__main__":

    if not os.path.exists('data'):
        os.mkdir('data')

    login.LoginScreen()
