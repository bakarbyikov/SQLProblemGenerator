from TableTask import *
from ChatBot import *
from QueryGenerator import *
from DatabaseConnector import *
from Task import *

import os
import random

def main():
    db_names = ["Book.db", "Car.db", "Planets.db"]
    
    #task2
    for i in range(45, 100):
        db_path = "dbs/" + random.choice(db_names)
        db_connector = DatabaseConnector(db_path)
        table_task = Table(db_connector.get_table_names_with_columns())
        generator = QueryGenerator(db_connector)
        
        random_query = generator.generate_random_query()
        result = db_connector.execute_query(random_query)
        
        path = f"bd_arhive/task_type_1/{i + 1}"
        os.makedirs(path)
        #return [random_query, task_from_query, result, random_query_remove]
        
        task2 = Task.generate_task_2(random_query, generator.columns_with_name_table, result)
        plt.savefig(path + f"/{i + 1}", dpi = 300)
        
        file_name = path + f"/{i + 1}.txt"
        with open(file_name, "w") as file:
            string = f"correct_query = {task2[0]};\nresult_query = {task2[2]};\ntask_query_txt = {task2[1]};\ntask_query_remove = {task2[3]}"
            file.write(string)  
         
        print(i)

    #task3
    for i in range(0, 100):
        db_path = "dbs/" + random.choice(db_names)
        db_connector = DatabaseConnector(db_path)
        table_task = Table(db_connector.get_table_names_with_columns())
        generator = QueryGenerator(db_connector)
        
        random_query = generator.generate_random_query()
        result = db_connector.execute_query(random_query)
        
        path = f"bd_arhive/task_type_2/{i + 1}"
        os.makedirs(path)
        #return [random_query, task_from_query, result, incorrect_querys]
        
        task3 = Task.generate_task_3(random_query, generator.columns_with_name_table, result)
        plt.savefig(path + f"/{i + 1}", dpi = 300)
        
        file_name = path + f"/{i + 1}.txt"
        with open(file_name, "w") as file:
            string = f"correct_query = {task3[0]};\nresult_query = {task3[2]};\ntask_query_txt = {task3[1]};\nincorrect_querys = {task3[3]}"
            file.write(string)  
         
        print(i)    
        
        
        
        

if __name__ == "__main__":
    main()

