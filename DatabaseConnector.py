import sqlite3
from itertools import chain, starmap
from os import getenv, listdir, path, remove
from time import sleep
from typing import NamedTuple

import psycopg2


class Column_info(NamedTuple):
    name: str
    type_: str
    
class Table_info(NamedTuple):
    name: str

class Database:
    def __init__(self) -> None:
        raise NotImplementedError

    def get_unique_letters(self, table_name: str, column_name: str) -> str:
        self.cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name};")
        letters = set()
        for name in self.cursor.fetchall():
            letters.update(*name)
        return ''.join(letters)
    
    def get_mininax(self, table_name: str, 
                           column_name: str) -> tuple[float|int]:
        query = f"SELECT MIN({column_name}), MAX({column_name}) FROM {table_name}"
        self.cursor.execute(query)
        return tuple(*self.cursor.fetchall())
    
    def get_random_values(self, table_name: str, column_name: str, n: int) -> tuple:
        query = f"SELECT {column_name} FROM {table_name} ORDER BY RANDOM() LIMIT {n};"
        self.cursor.execute(query)
        values, *_ = zip(*self.cursor.fetchall())
        return values
    
    def execute_query(self, query: str) -> list[tuple|int|str]:
        self.cursor.execute(query)
        try:
            result = self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None
        if result and len(result[0]) == 1:
            return list(chain.from_iterable(result))
        return result

class Sqlite3(Database):
    def __init__(self, name: str) -> None:
        self.connection = sqlite3.connect(f"dbs/{name}.db", 
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
    
    @staticmethod
    def get_db_list() -> list[str]:
        result = list()
        for raw_name in listdir("dbs"):
            if not raw_name.endswith(".db"):
                continue
            result.append(raw_name[:raw_name.rfind('.')])
        return result
    
    @staticmethod
    def create_database(scripts_path: str="db_create"):
        for raw_name in listdir(scripts_path):
            if not raw_name.endswith(".txt"):
                continue
            name, *_ = raw_name.rpartition(".")
            if path.isfile(f"dbs/{name}.db"):
                remove(f"dbs/{name}.db")
            db = Sqlite3(name)
            with open(path.join(scripts_path, raw_name), encoding="utf-8") as file:
                for query in file.read().split(";"):
                    db.execute_query(query)
        
    def get_tables_info(self) -> list[Table_info]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list()
        for name, *_ in self.cursor.fetchall():
            tables.append(Table_info(name))
        return tables
    
    def get_columns_info(self, table_name: str) -> list[Column_info]:
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = list()
        for _, name, type_, *_ in self.cursor.fetchall():
            columns.append(Column_info(name, type_))
        return columns

class PosgresSQL(Database):
    user = getenv("PG_USER")
    password = getenv("PG_PASSWORD")
    host = getenv("PG_HOST")
    port = getenv("PG_PORT")
    
    def __init__(self, name: str):
        self.connection = psycopg2.connect(
            dbname=name, user=self.user, password=self.password,
            host=self.host, port=self.port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
    
    @staticmethod
    def get_db_list() -> list[str]:
        query = """
            SELECT datname
            FROM pg_database
            WHERE datistemplate = 'f';
        """
        return PosgresSQL("postgres").execute_query(query)[1:]
    @staticmethod
    def create_database(scripts_path: str="db_create"):
        drop = """DROP DATABASE IF EXISTS "{name}";"""
        create = """
            CREATE DATABASE "{name}"
                WITH
                OWNER = postgres
                ENCODING = 'UTF8'
                LC_COLLATE = 'Russian_Russia.1251'
                LC_CTYPE = 'Russian_Russia.1251'
                LOCALE_PROVIDER = 'libc'
                TABLESPACE = pg_default
                CONNECTION LIMIT = -1
                IS_TEMPLATE = False
        """
        parent = PosgresSQL("postgres")
        for raw_name in listdir(scripts_path):
            if not raw_name.endswith(".txt"):
                continue
            name, *_ = raw_name.rpartition(".")
            parent.execute_query(drop.format(name=name))
            parent.execute_query(create.format(name=name))
            db = PosgresSQL(name)
            with open(path.join(scripts_path, raw_name), encoding="utf-8") as file:
                db.execute_query(file.read())
    
    def get_tables_info(self) -> list[Table_info]:
        query = """
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema not in ('information_schema', 'pg_catalog')
            AND table_type = 'BASE TABLE';
        """
        return list(map(Table_info, self.execute_query(query)))

    def get_columns_info(self, table_name: str) -> list[Column_info]:
        query = f"""
            SELECT column_name, data_type 
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """
        return list(starmap(Column_info, self.execute_query(query)))
    

if __name__ == "__main__":
    PosgresSQL.create_database()
    for name in PosgresSQL.get_db_list():
        db = PosgresSQL(name)
        print(name)
        for name, *_ in db.get_tables_info():
            print(name)
            print(db.get_columns_info(name))
            
    Sqlite3.create_database()
    for name in Sqlite3.get_db_list():
        db = Sqlite3(name)
        print(name)
        for name, *_ in db.get_tables_info():
            print(name)
            print(db.get_columns_info(name))

