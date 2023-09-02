import os
import json
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
        self.id = self.get_id(kwargs.get('id'))
        self.username: str = kwargs['username']
        self.password: str = kwargs['password']

    def get_id(self, id) -> str:
        if id is None:
            return str(uuid4())
        return id

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
    
    def __str__(self) -> str:
        return f"{self.username}"

    def save(self):
        users: list[UserDict] = self.read_db()
        users.append(self.to_dict)
        db = open(self.DB_PATH, 'w')
        json.dump(users, db)
        db.close()

    def delete(self):
        users: list[UserDict] = self.read_db()
        users.remove(self.to_dict)
        self.update_db(users)

    @classmethod
    def read_db(cls) -> list[UserDict]:
        if os.path.exists(cls.DB_PATH):
            db = open(cls.DB_PATH, 'r')
            data: list[UserDict] = json.load(db)
            db.close()
            return data

        db = open(cls.DB_PATH, 'w')
        json.dump([], db)
        return []

    @classmethod
    def update_db(cls, data: list[UserDict]) -> None:
        db = open(cls.DB_PATH, 'w')
        json.dump(data, db)
        db.close()

    @classmethod
    def get(cls, pk: str) -> UserDict:
        users: list[UserDict] = User.read_db()
        user: UserDict = next(filter(lambda user: user['id'] == pk, users))
        print(user)
        return user 


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

