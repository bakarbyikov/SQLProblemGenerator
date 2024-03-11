import random
import string

from DatabaseConnector import Database
from misc import Patterns


class Column:
    isnull = ["IS NULL", "IS NOT NULL"]
    def __init__(self, name: str, tabe_name: str, db: Database):
        self.name = name
        self.tabe_name = tabe_name
        self.db = db
    
    def create_condition(self) -> str:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return f"{str(type(self))[:-1]} {self.name}>"

class NumericColumn(Column):
    comparisons = ["<", "<=", ">=", ">"]
    def __init__(self, name: str, tabe_name: str, db: Database):
        super().__init__(name, tabe_name, db)
        self.min, self.max = self.db.get_mininax(self.tabe_name, self.name)
        self.is_int = isinstance(self.min, int)
    
    def create_condition(self) -> str:
        operator = random.choice(self.comparisons)
        if self.is_int:
            arg = random.randint(self.min, self.max)
        else:
            arg = random.uniform(self.min, self.max)
        
        return f"{self.name} {operator} {arg}"

class TextualColumn(Column):
    comparisons = ["LIKE", "NOT LIKE"]
    def __init__(self, name: str, tabe_name: str, db: Database):
        super().__init__(name, tabe_name, db)
        self.letters = self.db.get_unique_letters(self.tabe_name, self.name)

    def create_condition(self) -> str:
        operator = random.choice(self.comparisons)
        letter = random.choice(self.letters)
        arg = random.choice(list(Patterns)).value.format(letter)
        return f"{self.name} {operator} {arg}"

class BooleanColumn(Column):
    def create_condition(self) -> str:
        if random.randrange(2):
            return self.name
        return f"NOT {self.name}"

class DateColumn(Column):
    def create_condition(self) -> str:
        raise NotImplementedError

if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    c = NumericColumn("Birth_year", "Author", db)
    print(c.is_int)