import pandas as pd
import matplotlib.pyplot as plt

class Table:
    def __init__(self, tables):
        self.tables = tables 
        self.fig, self.ax = plt.subplots(figsize=(14, 2))
        df = pd.DataFrame([(table_name, ", ".join(self.tables[table_name])) for table_name in self.tables.keys()],
                          columns=["Table Name", "Columns"])
    
        table = self.ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        self.ax.axis('off')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))
        table.scale(1, 1.5)
    
    def get_table(self):
        return plt

if __name__ == "__main__":
    from DatabaseConnector import Sqlite3
    db = Sqlite3("dbs/Book.db")
    table = Table(db.get_table_names_with_columns())
    table.get_table().show()    