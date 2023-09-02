import os
from screens import login


if __name__ == "__main__":

    if not os.path.exists('data'):
        os.environ['USER_DB_PATH'] = 'data/users.json'

    login.LoginScreen()
