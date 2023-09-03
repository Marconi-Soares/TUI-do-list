import os
import hashlib
from uuid import uuid4
from typing import TypedDict


class UserDict(TypedDict):
    id: str
    username: str
    password: str


class User:
    DB_PATH: str = os.environ.get('USER_DB_PATH', 'tests/db/user_db.json')

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
        if self.username is None:
            return False

        if self.password is None:
            return False

        return True

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }
