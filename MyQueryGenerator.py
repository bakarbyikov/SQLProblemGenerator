import random

from misc import Column_type, Comparisons
from Table import Table


class QueryGenerator:
    def __init__(self, table: Table):
        self.table = table
    
    def create_selection(self) -> str:
        return ", ".join(self.create_args())
    
    def create_args(self) -> list[str]:
        n_args = random.randint(1, len(self.table.columns))
        choosen = random.sample(self.table.columns, k=n_args)
        return [column.name for column in choosen]
    
    def create_where(self) -> str:
        parts = ["WHERE"]
        n_conditions = random.randint(1, len(self.table.columns))
        choosen = random.sample(self.table.columns, k=n_conditions)
        for column in choosen:
            parts.append(column.create_condition())
            parts.append(random.choice(Comparisons[Column_type.boolean]))
        assert len(parts) >= 1
        parts.pop()
        return " ".join(parts)
    
    def generate(self, seed: int=None):
        random.seed(seed)
        parts = [
            "SELECT",
            self.create_selection(),
            "FROM",
            self.table.name,
            self.create_where()
            ]
        return " ".join(parts)


if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    table = Table(db, "Author")
    gen = QueryGenerator(table)
    for i in range(10**4):
        query = gen.generate()
        print(query)
        res = db.execute_query(query)
