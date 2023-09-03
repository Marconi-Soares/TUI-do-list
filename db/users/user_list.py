import os
from .user import User
from db.db import DB


class UserList(DB):
    DB_PATH: str = os.environ.get('USER_DB_PATH', 'tests/db/user_db.json')

    def __len__(self) -> int:
        return len(self.users)

    @classmethod
    def append(cls, user: User) -> None:
        """
        Verifica se o usuário pode ser salvo e o salva.
        Um usuário não pode ser salvo caso:
            - O atributo "is_saveble" seja falso;
            - Já exista um usuário com o mesmo username;
        """
        if not user.is_saveble:
            raise ValueError("Este usuário não pode ser salvo")

        users: list[dict[str, str]] = DB.load_data(cls.DB_PATH)

        try:
            cls.get('username', user.username)
            raise ValueError(f"'{user}' já está sendo usado.")
        except StopIteration:
            pass

        user_dict: dict[str, str] = {"password": user.password, **user.to_dict}
        users.append(user_dict)
        DB.write_db(cls.DB_PATH, users)

    @classmethod
    def remove(cls, pk: str) -> None:
        user_dicts: list[dict] = DB.load_data(cls.DB_PATH)
        try:
            user = next(filter(lambda user: user['id'] == pk, user_dicts))
            user_dicts.remove(user)
            DB.write_db(cls.DB_PATH, user_dicts)
            return
        except:
            print("Nenhum usuário encontrado")

    def all(self):
        return self.load_data(self.DB_PATH)

    @classmethod
    def get(cls, field: str, value: str | int, to_dict=False):
        user: dict[str, str] | None = DB.get(cls.DB_PATH, field, value)

        if to_dict:
            return user

        if user:
            return User(**user)

    @property
    def users(self) -> list[User]:
        return [
            User(**user_dict)
            for user_dict in self.load_data(self.DB_PATH)
        ]

    def __getitem__(self, item: int) -> User:
        return self.users[item]
