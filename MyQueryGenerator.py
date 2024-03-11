import random
import string
from DatabaseConnector import DatabaseConnector
from misc import Column, Table, Comparisons, Column_type


class QueryGenerator:
    def __init__(self, database: DatabaseConnector):
        self.db = database
    
    def create_args(self, table: Table) -> list[str]:
        n_args = random.randint(1, len(table.columns))
        choosen = random.sample(table.columns, k=n_args)
        return [column.name for column in choosen]
    
    def create_condition(self, column: Column) -> str:
        if column.type_ not in Comparisons:
            raise NotImplementedError
        operator = random.choice(Comparisons[column.type_])
        match column.type_:
            case Column_type.numeric:
                arg = random.randrange(1000)
            case Column_type.textual:
                arg = f"'%{random.choice(string.ascii_lowercase)}%'"
            case Column_type.boolean:
                raise NotImplementedError
        return f"{column.name} {operator} {arg}"
    
    def create_where(self, table: Table) -> str:
        query = ["WHERE"]
        n_conditions = random.randint(1, len(table.columns))
        choosen = random.sample(table.columns, k=n_conditions)
        for i, column in enumerate(choosen):
            query.append(self.create_condition(column))
            query.append(random.choice(Comparisons[Column_type.boolean]))
        assert len(query) >= 1
        query.pop()
        return " ".join(query)
    
    def generate(self, seed: int=None):
        random.seed(seed)
        query = ["SELECT"]

        table = random.choice(self.db.get_tables())

        args = self.create_args(table)
        query.append(", ".join(args))

        query.append("FROM")
        query.append(table.name)

        query.append(self.create_where(table))

        return " ".join(query)


if __name__ == "__main__":
    db = DatabaseConnector("dbs/Book.db")
    gen = QueryGenerator(db)
    for i in range(50):
        try:
            print(gen.generate())
        except NotImplementedError:
            pass