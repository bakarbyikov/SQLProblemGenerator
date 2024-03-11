import random

from misc import Patterns


class Column:
    def __init__(self, name: str):
        self.name = name
    
    def create_condition(self) -> str:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return f"{str(type(self))[:-1]} {self.name}>"

class NumericColumn(Column):
    comparisons = ["<", "<=", ">=", ">"]
    def __init__(self, name: str, min: int|float, max: int|float):
        self.min, self.max = min, max
        self.is_int = isinstance(min, int)
        super().__init__(name)
    
    def create_condition(self) -> str:
        operator = random.choice(self.comparisons)
        if self.is_int:
            arg = random.randint(self.min, self.max)
        else:
            arg = random.uniform(self.min, self.max)
        
        return f"{self.name} {operator} {arg}"

class TextualColumn(Column):
    comparisons = ["LIKE", "NOT LIKE"]
    def __init__(self, name: str, letters: str):
        self.letters = letters
        super().__init__(name)

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
    c = Column("Oleg")
    print(c)