import random
from typing import NamedTuple

from tqdm import tqdm

from Column import Column
from misc import interlay
from Table import Table


class Segment(NamedTuple):
    start: int
    end: int

    def rvs(self):
        return random.randint(*self)

class Query_settings(NamedTuple):
    n_args: Segment
    add_distinct: bool
    add_aggregation: bool
    n_conditions: Segment
    n_orders: Segment
    limit: Segment
    offset: Segment

class QueryGenerator:
    def __init__(self, table: Table):
        self.table = table
    
    def choose_columns(self, n_args: Segment) -> list[Column]:
        return random.sample(self.table.columns, k=n_args.rvs())
    
    def create_selection(self, columns: list[Column]) -> list[str]:
        return list(map(Column.get_name, columns))
    
    def create_aggregation(self, columns: list[Column]) -> list[str]:
        return list(map(Column.create_aggregation, columns))
    
    def create_where(self, n_conditions: Segment) -> str:
        parts = ["WHERE"]
        n_cond = random.randint(*n_conditions)
        choosen = random.sample(self.table.columns, k=n_cond)
        parts.extend(interlay(map(Column.create_condition, choosen),
                              random.choices(["AND", "OR"], k=n_cond)))
        return " ".join(parts)
    
    def create_order(self, columns: list[str], n_orders: Segment) -> str:
        order_by = random.sample(columns, k=min(len(columns), n_orders.rvs()))
        parts = list()
        for c in order_by:
            if random.randrange(2):
                parts.append(c)
            else:
                parts.append(f"{c} DESC")
        return f"ORDER BY {", ".join(parts)}"
    
    def create_limit(self, limit: Segment) -> str:
        return f"LIMIT {limit.rvs()}"
    
    def create_offset(self, offset: Segment) -> str:
        return f"OFFSET {offset.rvs()}"

    def generate(self, settings: Query_settings, seed: int=None) -> str:
        random.seed(seed)
        parts = ["SELECT"]
        if settings.add_aggregation == settings.add_distinct:
            raise ValueError("Cant create query with DISTINCT and AGGREGATION")
        if settings.add_distinct:
            parts.append("DISTINCT")

        selected = self.choose_columns(settings.n_args)
        if settings.add_aggregation:
            expression, columns = zip(*self.create_aggregation(selected))
        else:
            expression = columns = self.create_selection(selected)
        parts.append(", ".join(expression))

        parts.append("FROM")
        parts.append(self.table.name)

        if settings.n_conditions.end:
            parts.append(self.create_where(settings.n_conditions))
        if settings.n_orders.end:
            parts.append(self.create_order(columns, settings.n_orders))
        if settings.limit.end:
            parts.append(self.create_limit(settings.limit))
        if settings.offset.end:
            parts.append(self.create_offset(settings.offset))
        return " ".join(parts)
    
    def self_test(self, n_tests: int=10**3, aggregation: bool=None):
        if aggregation is None:
            self.self_test(n_tests//2, True)
            self.self_test(n_tests//2, False)
            return
        settings = Query_settings(
            n_args=Segment(1, self.table.n_columns),
            add_distinct=not aggregation,
            add_aggregation=aggregation,
            n_conditions=Segment(1, self.table.n_columns),
            n_orders=Segment(1, 2),
            limit=Segment(1, 2),
            offset=Segment(1, 2)
        )
        for _ in tqdm(range(n_tests)):
            query = self.generate(settings)
            try:
                self.table.db.execute_query(query)
            except Exception:
                print(f"{self.table.name = }")
                print(f"{query = }")
                raise

def full_test(n_test_per_table: int=10**3):
    from DatabaseConnector import PosgresSQL
    for db_name in PosgresSQL.get_db_list():
        db = PosgresSQL(db_name)
        print(db_name)

        for tb_info in db.get_tables_info():
            print(tb_info.name)
            table = Table(db, tb_info.name)
            gen = QueryGenerator(table)
            gen.self_test(n_test_per_table)

if __name__ == "__main__":
    full_test(10**3)

