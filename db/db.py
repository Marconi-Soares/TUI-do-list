from typing import Any
import os
import json


class DB:
    @classmethod
    def load_data(cls, DB_PATH: str) -> list| list[dict]:
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
    def get(cls, DB_PATH, field: str, value) -> dict|None:
        data_list: list[dict] = cls.load_data(DB_PATH)

        try:
            return next(filter(lambda data: data[field] == value, data_list))
        except StopIteration:
            print('Não encontrado')
        except KeyError:
            print('Campo inválido')

    @classmethod
    def write_db(cls, DB_PATH, data: Any):
        db = open(DB_PATH, 'w')
        json.dump(data, db)
        db.close()
