from enum import Enum
from itertools import chain
from typing import Any, Generator, Sequence

def interlay(outer: Sequence, inner: Sequence) -> Generator[Any, None, None]:
    outer = iter(outer)
    yield next(outer)
    yield from chain.from_iterable(zip(inner, outer))

class Column_type(Enum):
    numeric = "INTEGER"
    textual = "TEXT"
    boolean = "BOOLEAN"
    date = "DATE"

Comparisons = {
    Column_type.numeric: ["<", "<=", ">=", ">"],
    Column_type.textual: ["LIKE", "NOT LIKE"],
    Column_type.boolean: ["AND", "OR"],
    Column_type.date: [],
}

class Patterns(Enum):
    Starts_with = "'{}%'"
    Ends_with = "'%{}'"
    Contains = "'%{}%'"


def add_apostrophe(string: str) -> str:
    return f"'{string}'"

if __name__ == "__main__":
    print(*interlay(range(5), "-"*30))