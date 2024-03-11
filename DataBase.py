from os import getenv
import psycopg2


class DataBase:
    user = getenv("PG_USER")
    password = getenv("PG_PASSWORD")
    host = getenv("PG_HOST")
    port = getenv("PG_PORT")

    def __init__(self, dbname: str):
        self.connection = psycopg2.connect(
            dbname=dbname, user=self.user, password=self.password,
            host=self.host, port=self.port
            )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
    
    def list_tables(self) -> list[str]:
        query = """
            SELECT
                table_schema || '.' || table_name
            FROM
                information_schema.tables
            WHERE
                table_type = 'BASE TABLE'
            AND
                table_schema NOT IN ('pg_catalog', 'information_schema');
                """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def create_database(self, name: str):
        self.cursor.execute(f"CREATE DATABASE {name}")
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    db = DataBase("baba")
    # db.create_database("oleg")
    print(db.list_tables())