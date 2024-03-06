import random
from datetime import datetime

class QueryGenerator:
     def __init__(self, database_connector):
        self.db_connector = database_connector
        self.tables = self.db_connector.get_table_names_with_columns()
        self.columns_with_name_table = None

     def generate_random_query(self):
        table_name = random.choice(list(self.tables.keys()))
        columns_from_table = self.tables[table_name]
        self.columns_with_name_table = list([table_name] + columns_from_table)
        
        if random.choices([1, 2], weights=[0.3, 0.7])[0] == 2:
            column1, column2 = random.sample(columns_from_table, 2)
        else:
            column1 = column2 = random.choice(columns_from_table)
        
        table_info_query = f"PRAGMA table_info({table_name});"
        column_info = {info[1]: info[2] for info in self.db_connector.execute_query(table_info_query)}

        values_query1 = f"SELECT DISTINCT {column1} FROM {table_name};"
        values1 = [value[0] for value in self.db_connector.execute_query(values_query1)]

        values_query2 = f"SELECT DISTINCT {column2} FROM {table_name};"
        values2 = [value[0] for value in self.db_connector.execute_query(values_query2)]

        def is_text(column):
            return column_info.get(column, '') == "TEXT"
    
        def is_bool(column):
            values_query = f"SELECT DISTINCT {column} FROM {table_name};"
            distinct_values = set(value[0] for value in self.db_connector.execute_query(values_query))
            return len(list(distinct_values)) == 2

        def is_time(column):
            try:
                 time_values_query = f"SELECT DISTINCT {column} FROM {table_name};"
                 datetime.strptime(str(self.db_connector.execute_query(time_values_query)[0]), '%H:%M:%S')
                 return True
            except ValueError:
                return False

        select_operator = "SELECT"
        where_clause = ""; condition = "";
        types_operators = ["=", "!=", "<", "<=", ">=", ">"]

        two_logical = random.choices([1, 2], weights=[0.3, 0.7])[0]
        if two_logical == 2: 
            logical_operator = random.choice(["AND", "OR"])
            condition_type1, condition_type2 = random.choice(types_operators), random.choice(types_operators)
            other_value1, other_value2 = random.choice(values1), random.choice(values2)

            if is_text(column1) or is_bool(column1) or is_time(column1):
                condition_type1 = random.choice(["=", "!="])     
            condition += f"{column1} {condition_type1} '{other_value1}'"

            off_validate_and_or = [("<", ">"), ("<=", ">="), ("<=", "<"), ("<=", ">"), ("<", ">="), ("<", "<="), 
                                    (">=", ">"), (">", ">="), ("<", "<"), (">", ">"), 
                                    ("<=", "<="), (">=", ">=")]

            if (column1 == column2):
                while (("=" in (condition_type1, condition_type2))) \
                or ((condition_type1, condition_type2) in off_validate_and_or):
                    condition_type1, condition_type2 = random.choice(types_operators), random.choice(types_operators)
        
            if is_text(column2) or is_bool(column2) or is_time(column2):
                condition_type2 = random.choice(["=", "!="])  
            
            if (values1 != values2):
                condition += f" {logical_operator} {column2} {condition_type2} '{other_value2}'"
        else:
            condition_type = random.choice(types_operators)
            random_value = random.choice(values1)
            if is_text(column1) or is_bool(column1) or is_time(column1):
                condition_type = random.choice(["=", "!="])

            condition = f"{column1} {condition_type} '{random_value}'"

        where_clause = f" WHERE {condition}"

        add_Group_By = True
        if (add_Group_By):
                aggregate_functions = ["COUNT", "MAX", "MIN", "SUM", "AVG"] 
                aggregate_function = random.choice(aggregate_functions)
                group_by_clause = f" GROUP BY {column1}"
    
        if add_Group_By:
            if (column1 == column2) or (two_logical == 1):
                query = f"{select_operator} {column1} FROM {table_name}{where_clause}"
            else:
                if ((column1 != column2) and (two_logical == 2) and ("Id" not in column2)
                        and (((column_info.get(column2, '') == "INTEGER")) or aggregate_function == "COUNT")):
                    query = f"{select_operator} {column1}, {aggregate_function}({column2}) FROM {table_name}{where_clause}{group_by_clause}"
                else:
                    query = f"{select_operator} {column1}, {column2} FROM {table_name}{where_clause}"
        else:
            if (column1 == column2) or (two_logical == 1):
                query = f"{select_operator} {column1} FROM {table_name}{where_clause}"
            else:
                query = f"{select_operator} {column1}, {column2} FROM {table_name}{where_clause}"

        for attribute in self.columns_with_name_table.copy():
            if (attribute not in query.split(" ")):
                self.columns_with_name_table.remove(attribute)
        
        return query




