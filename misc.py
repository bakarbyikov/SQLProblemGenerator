from enum import Enum


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