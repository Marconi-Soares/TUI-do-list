import os
import json
import hashlib
from uuid import uuid4
from typing import TypedDict
from .db import DB


class UserDict(TypedDict):
    id: str
    username: str
    password: str


class User:
    DB_PATH: str = "data/users.json"

    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get("id")
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
    
    def __str__(self) -> str:
        return f"{self.username}"

    @property
    def id(self) -> str:
        return str(self._id)

    @id.setter
    def id(self, value: str|None) -> None:
        """
        Caso um id seja passado durante a criação do User,
        assume-se que é apenas uma serialização.
        """
        if value is None:
            self._id = str(uuid4())
        else:
            self._id = value

    @property
    def password(self) -> str|None:
        return self._password

    @password.setter
    def password(self, value: str|None) -> None:
        """
        Se a senha não for None gera o hash da senha e salva
        no banco de dados. O suporte ao None é para possibilitar
        a serialização que é feita apenas com os atributos id e username
        """
        if value is None:
            self._password = None
            return

        hash_obj = hashlib.sha512()
        hash_obj.update(value.encode('utf-8'))
        self._password = hash_obj.hexdigest()

    @property
    def is_saveble(self) -> bool:
        """
        Se a senha ou o nome de usuário não forem providos
        o usuário não pode ser salvo no banco de dados.
        Esse atributo permite diferenciar um usuário serializado
        (sem senha) de um usuário instanciado (com senha)
        """
        if self.password is None:
            return False
        return True

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }
    

class UserList(DB):
    DB_PATH: str = "data/users.json"

    def __len__(self) -> int: 
        return len(self.users)

    @classmethod
    def append(cls, user: User) -> None: 
        users: list[dict[str, str]] = DB.load_data(cls.DB_PATH)
        users.append(user.to_dict)
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
    def get(cls, field: str, value: str|int, to_dict=False):
        user: dict[str, str]|None = DB.get(cls.DB_PATH, field, value)

        if to_dict:
            return user

        if user:
            return User(**user)

    @property
    def users(self):
        return [
            User(**user_dict)
            for user_dict in self.load_data(self.DB_PATH)
        ]

    def __getitem__(self, item: int):
        return self.users[item]
