import sqlite3

class DatabaseConnector:
    def __init__(self, database_path):
        self.con = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.con.cursor()

    def get_table_names_with_columns(self):
        tables = {}
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [table[0] for table in self.cursor.fetchall()]

        for table_name in table_names:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            tables[table_name] = [column[1] for column in self.cursor.fetchall()]
        return tables

    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result





