import random

from DatabaseConnector import Database
from misc import Patterns, add_apostrophe


class Column:
    isnull = ["IS NULL", "IS NOT NULL"]

    def __init__(self, name: str, tabe_name: str, db: Database):
        self.name = name
        self.tabe_name = tabe_name
        self.db = db
        self.creaters = [self.create_null]
    
    def create_null(self) -> str:
        operator = random.choice(self.isnull)
        return f"{self.name} {operator}"
    
    def create_condition(self) -> str:
        return random.choice(self.creaters)()
    
    def __repr__(self) -> str:
        return f"{str(type(self))[:-1]} {self.name}>"

class NumericColumn(Column):
    comparisons = ["<", "<=", ">=", ">"]
    between = ["BETWEEN", "NOT BETWEEN"]
    in_ = ["IN", "NOT IN"]
    
    def __init__(self, name: str, tabe_name: str, db: Database):
        super().__init__(name, tabe_name, db)
        self.creaters.extend([self.create_between, self.create_comparison, self.create_in])
        
    def create_in(self) -> str:
        operator = random.choice(self.in_)
        n_values = random.randrange(2, 5)
        values = self.db.get_random_values(self.tabe_name, self.name, n_values)
        return f"{self.name} {operator} ({", ".join(map(str, values))})"
    
    def create_between(self) -> str:
        operator = random.choice(self.between)
        left, right = sorted(self.db.get_random_values(self.tabe_name, self.name, 2))
        return f"{self.name} {operator} {left} AND {right}"
    
    def create_comparison(self) -> str:
        operator = random.choice(self.comparisons)
        value, *_ = self.db.get_random_values(self.tabe_name, self.name, 1)
        return f"{self.name} {operator} {value}"

class TextualColumn(Column):
    mathcing = ["LIKE", "NOT LIKE"]
    in_ = ["IN", "NOT IN"]

    def __init__(self, name: str, tabe_name: str, db: Database):
        super().__init__(name, tabe_name, db)
        self.letters = self.db.get_unique_letters(self.tabe_name, self.name)
        self.creaters.append(self.create_mathcing)
        
    def create_in(self) -> str:
        operator = random.choice(self.in_)
        n_values = random.randrange(2, 5)
        values = self.db.get_random_values(self.tabe_name, self.name, n_values)
        return f"{self.name} {operator} ({", ".join(map(add_apostrophe, values))})"
    
    def create_mathcing(self) -> str:
        operator = random.choice(self.mathcing)
        letter = random.choice(self.letters)
        arg = random.choice(list(Patterns)).value.format(letter)
        return f"{self.name} {operator} {arg}"

class BooleanColumn(Column):
    inversion = ["", "NOT"]
    def __init__(self, name: str, tabe_name: str, db: Database):
        super().__init__(name, tabe_name, db)
        self.creaters.append(self.create_simple)
    
    def create_simple(self) -> str:
        operator = random.choice(self.inversion)
        return f"{operator} {self.name}"

class DateColumn(Column):
    pass

if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    c = NumericColumn("Birth_year", "Author", db)
    print(c.is_int)