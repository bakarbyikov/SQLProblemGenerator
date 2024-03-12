from itertools import filterfalse
from typing import Self

from Column import (BooleanColumn, Column, DateColumn, NumericColumn,
                    TextualColumn)
from DatabaseConnector import Column_info, Database


class Table:

    def __init__(self, db: Database, name: str) -> None:
        self.db = db
        self.name = name
        self.columns = self.init_columns()
        self.order_columns = self.filter_order(self)
    
    @classmethod
    def from_database(cls, db: Database) -> list[Self]:
        return [cls(db, *name) for name in db.get_tables_info()]
    
    def parse_column(self, column: Column_info) -> Column:
        match column.type_:
            case "INTEGER":
                column_class = NumericColumn
            case "TEXT":
                column_class = TextualColumn
            case "BOOLEAN":
                column_class = BooleanColumn
            case "DATE":
                column_class = DateColumn
            case _:
                raise ValueError(f"Not supported column type: {column.type_}")
        return column_class(column.name, self.name, self.db)
    
    def init_columns(self) -> list[Column]:
        columns = self.db.get_columns_info(self.name)
        return [self.parse_column(column) for column in columns]
    
    def filter_order(self) -> list[Column]:
        return list(filterfalse(lambda c: isinstance(c, DateColumn), self.columns))
    
    def __repr__(self) -> str:
        return f"<Table {self.name}, columns = {self.columns}"

if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    for table in Table.from_database(db):
        print(table)