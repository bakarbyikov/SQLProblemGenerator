import sqlite3
from typing import NamedTuple


class Column_info(NamedTuple):
    name: str
    type_: str
    
class Table_info(NamedTuple):
    name: str

class Database:
    def get_tables_info(self) -> list[Table_info]:
        raise NotImplementedError
    
    def get_columns_info(self, table_name: str) -> list[Column_info]:
        raise NotImplementedError
    
    def get_column_mininax(self, table_name: str, 
                           column_name: str) -> tuple[float|int]:
        raise NotImplementedError
    
class Sqlite3(Database):
    def __init__(self, database_path: str):
        self.con = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.con.cursor()
    
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
    
    def get_column_mininax(self, table_name: str, 
                           column_name: str) -> tuple[float|int]:
        query = f"SELECT MIN({column_name}), MAX({column_name}) FROM {table_name}"
        self.cursor.execute(query)
        return tuple(*self.cursor.fetchall())
    
    
    def get_table_names_with_columns(self):
        tables = {}
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [table[0] for table in self.cursor.fetchall()]

        for table_name in table_names:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            tables[table_name] = [column[1] for column in self.cursor.fetchall()]
        return tables
    
    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


if __name__ == "__main__":
    for name in ("dbs/Car.db", "dbs/Planets.db", "dbs/Book.db"):
        db = Sqlite3(name)
        print(name)
        for name, *_ in db.get_tables_info():
            print(name)
            print(db.get_columns_info(name))

    print(db.get_column_mininax("Author", "Birth_year"))