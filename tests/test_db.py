import os
import json
from db.db import DB
from typing import Any
from io import TextIOWrapper
from tests.test_user import AbstractTestCase


class TestDB(AbstractTestCase):
    PATH: str = 'tests/db/db.json'

    def _read_data(self) -> Any:
        db: TextIOWrapper = open(self.PATH)
        data: Any = json.load(db)
        db.close()
        return data

    def _fill_data(self, data: list[dict]) -> None:
        db: TextIOWrapper = open(self.PATH, 'w')
        json.dump(data, db)
        db.close()

    def test_load_db_is_creating_json_file_when_empty(self):
        """
        Ao tentar carregar um um arquivo de banco de dados que não existe,
        um novo deve ser criado e uma lista vazia deve ser retornada.
        """
        self.assertFalse(os.path.exists(self.PATH))
        data: list = DB.load_data(self.PATH)
        self.assertListEqual(data, [])
        self.assertTrue(os.path.exists(self.PATH))

    def test_load_db_do_not_create_another_file_if_not_empty(self):
        """
        Ao carregar um arquivo que existe, deve retornar as informação desse
        arquivo.
        """
        temp_data: list[dict[str, str]] = [{'test': 'data test'}]
        self._fill_data(temp_data)
        data: list[dict[str, str]] = DB.load_data(self.PATH)
        self.assertListEqual(data, temp_data)

    def test_write_db(self):
        self.assertFalse(os.path.exists(self.PATH))
        data_to_write: list[dict[str, str]] = [{'test': 'data test'}]
        DB.write_db(self.PATH, data_to_write)
        data: Any = self._read_data()
        self.assertTrue(os.path.exists(self.PATH))
        self.assertListEqual(data, data_to_write)

    def test_write_db_only_write_lists(self):
        """
        Apenas listas podem ser adicionados ao banco de dados.
        """
        self.skipTest('Must be implemented')
        with self.assertRaises(ValueError):
            DB.write_db(self.PATH, {})

    def test_write_db_only_write_list_of_dicts(self):
        """
        Apenas list[dict] podem ser adicionados ao banco.
        """
        self.skipTest('Must be implemented')
        with self.assertRaises(ValueError):
            DB.write_db(self.PATH, [1, 2, 3])

    def test_get_not_found(self):
        """
        Ao não encontrar o item que dê match com o campo e valor
        passado, deve resultar num erro StopIteration
        """
        self.skipTest('Must be implemented')
        with self.assertRaises(StopIteration):
            DB.get(self.PATH, 'invalid', 'xxxx')

    def test_get_invalid_key(self):
        """
        Ao não conseguir pesquisar no campo solicitado, deve
        resultar num erro KeyError
        """
        self.skipTest('Must be implemented')
        with self.assertRaises(KeyError):
            DB.get(self.PATH, 'invalid', 'xxxx')

    def test_get_return_the_searched_item(self):
        data_list: list = []
        data_to_search: dict[str, str] = {'id': '123'}
        data_list.append(data_to_search)
        self._fill_data(data_list)
        self.assertEqual(DB.get(self.PATH, 'id', '123'), data_to_search)
