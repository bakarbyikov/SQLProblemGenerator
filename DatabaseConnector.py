from pprint import pprint
import sqlite3

from misc import Column, Column_type, Table

class DatabaseConnector:
    def __init__(self, database_path: str):
        self.con = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.con.cursor()
        self.tables = list()
    
    def get_tables(self) -> list[Table]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list()
        for name, *_ in self.cursor.fetchall():
            tables.append(Table(name, tuple(self.get_columns(name))))
        return tables
    
    def get_columns(self, table_name: str) -> list[Column]:
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = list()
        for _, name, type_, *_ in self.cursor.fetchall():
            columns.append(Column(name, Column_type(type_)))
        return columns

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
    for name in ("dbs/Book.db", "dbs/Car.db", "dbs/Planets.db"):
        db = DatabaseConnector(name)
        print(name)
        pprint(db.get_tables())