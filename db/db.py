import os
import json
from typing import Any


def data_is_saveble(data: list[dict]) -> None:
    if not isinstance(data, list):
        raise ValueError('Only can be saved to database.')

    if not all(isinstance(item, dict) for item in data):
        raise ValueError('Only dicts can be saved to the database.')


class DB:
    @classmethod
    def load_data(cls, DB_PATH: str) -> list | list[dict]:
        if not os.path.exists(DB_PATH):
            db = open(DB_PATH, 'w')
            json.dump([], db)
            db.close()
            return []

        db = open(DB_PATH, 'r')
        data: list[dict] = json.load(db)
        db.close()
        return data

    @classmethod
    def get(cls, DB_PATH, field: str, value) -> dict | None:
        data_list: list[dict] = cls.load_data(DB_PATH)

        return next(filter(
            lambda data: data[field] == value, data_list
        ))

    @classmethod
    def write_db(cls, DB_PATH, data: Any):
        data_is_saveble(data)

        db = open(DB_PATH, 'w')
        json.dump(data, db)
        db.close()
