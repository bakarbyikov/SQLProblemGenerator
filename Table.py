import string
from typing import Self

from Column import (BooleanColumn, Column, DateColumn, NumericColumn,
                    TextualColumn)
from DatabaseConnector import Column_info, Database


class Table:

    def __init__(self, db: Database, name: str) -> None:
        self.db = db
        self.name = name
        self.columns = self.init_columns()
    
    @classmethod
    def from_database(cls, db: Database) -> list[Self]:
        return [cls(db, *name) for name in db.get_tables_info()]
    
    def parse_column(self, column: Column_info) -> Column:
        if column.type_ == "INTEGER":
            min_, max_ = self.db.get_column_mininax(self.name, column.name)
            return NumericColumn(column.name, min_, max_)
        if column.type_ == "TEXT":
            letters = string.ascii_lowercase
            return TextualColumn(column.name, letters)
        if column.type_ == "BOOLEAN":
            return BooleanColumn(column.name)
        if column.type_ == "DATE":
            return DateColumn(column.name)
    
    def init_columns(self) -> list[Column]:
        columns = self.db.get_columns_info(self.name)
        return [self.parse_column(column) for column in columns]
    
    def __repr__(self) -> str:
        return f"<Table {self.name}, columns = {self.columns}"

if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    for table in Table.from_database(db):
        print(table)