from TableTask import *
from ChatBot import *
from QueryGenerator import *
from DatabaseConnector import *
import math
import random

class Task:
    @staticmethod
    def generate_task_1(random_query, columns_with_name_table, result):
        task_from_query = ChatBot.get_task_from_query(random_query, columns_with_name_table) + \
            " Напишите соответствующий запрос чтобы получить нужный результат."
        return [random_query, task_from_query, result]
    
    @staticmethod
    def generate_task_2(random_query, columns_with_name_table, result):
        random_query_remove = random_query.replace("GROUP BY", "GROUPBY").split(" ")
        
        operators_to_replace = ["=", "!=", "<", "<=", ">=", ">"]
        keywords_to_replace1 = ["SELECT", "WHERE", "FROM", "GROUPBY", "AND", "OR"]
        keywords_to_replace2 = ["MAX", "MIN", "SUM", "AVG", "COUNT"]
        keywords_to_replace2 = [element for element in keywords_to_replace2 if element in random_query]
        
        replace_elements = operators_to_replace + keywords_to_replace1 + columns_with_name_table
        replace_elements = [element for element in replace_elements if element in random_query_remove]
        replace_elements.extend(keywords_to_replace2)
        
        ceil_or_floor = random.choice(["<", ">", ">"])
        if ceil_or_floor == ">":
            num_to_remove = math.ceil(math.log(len(replace_elements), 2))   
        else:
            num_to_remove = math.floor(math.log(len(replace_elements), 2))
        replace_elements = random.sample(replace_elements, k = num_to_remove)
        
        for element in replace_elements:
            direction = random.choice(["end", "start"])

            if element not in keywords_to_replace2:
                if direction == "start":
                     element_index = random_query_remove.index(element)
                else:
                     element_index = len(random_query_remove) - random_query_remove[-1::-1].index(element) - 1
            else:
                 element_index = [index for index, element_full in enumerate(random_query_remove) if element in element_full][0]

            random_query_remove[element_index] = random_query_remove[element_index].replace(element, "_")


        random_query_remove = ' '.join(random_query_remove).replace("GROUPBY", "GROUP BY")
        task_from_query = ChatBot.get_task_from_query(random_query, columns_with_name_table) + \
            " Заполните пропуски в запросе чтобы получить нужный результат."
        return [random_query, task_from_query, result, random_query_remove]
    
    @staticmethod
    def generate_task_3(random_query, columns_with_name_table, result):
        operators_to_replace = ["=", "!=", "<", "<=", ">=", ">"]
        keywords_to_replace2 = ["MAX", "MIN", "SUM", "AVG", "COUNT"]
        
        incorrect_querys = []
        
        for i in range(3):
            while True:
                incorrect_query = random_query.replace("GROUP BY", "GROUPBY")
                incorrect_query_split = incorrect_query.split(" ")
                
                incorrect_skip_keywords = random.choices([True, False], weights=[0.4, 0.6])[0]
                if incorrect_skip_keywords:
                    if "GROUPBY" in incorrect_query:
                        skip_keywords = ["FROM", "SELECT", "GROUPBY"]
                    else:
                        skip_keywords = ["FROM", "SELECT"]
                    random_skip_keywords = random.choice(skip_keywords)
                    
                    if random_skip_keywords == "FROM":
                        index_from = incorrect_query_split.index("FROM")
                        incorrect_query_split = incorrect_query_split[:index_from] + incorrect_query_split[index_from + 2:]
                    elif random_skip_keywords == "SELECT":
                        index_from = incorrect_query_split.index("FROM")
                        incorrect_query_split = incorrect_query_split[index_from:]
                    elif random_skip_keywords == "GROUPBY":
                        incorrect_query_split = incorrect_query_split[:-2]
                    incorrect_query = ' '.join(incorrect_query_split)
                    incorrect_query = incorrect_query.replace("GROUPBY", "GROUP BY")
                    
                    if (incorrect_query == random_query) or (incorrect_query in incorrect_querys):
                        continue
                    incorrect_querys.append(incorrect_query)
                    break

                incorrect_and_or = random.choice([True, False])
                if incorrect_and_or:
                    if "AND" in incorrect_query:
                        incorrect_query = incorrect_query.replace("AND", "OR")
                        incorrect_query_split = incorrect_query.split(" ")
                    else:
                        incorrect_query = incorrect_query.replace("OR", "AND")
                        incorrect_query_split = incorrect_query.split(" ")

                incorrect_group_by_column = random.choices([True, False], weights=[0.7, 0.3])[0]
                if (incorrect_group_by_column == True) and ("GROUPBY" in incorrect_query):
                    incorrect_query_split[-1] = incorrect_query_split[2].split("(")[1].replace(")", "")
                    incorrect_query = ' '.join(incorrect_query_split)
                
                incorrect_aggregate = random.choices([True, False], weights=[0.7, 0.3])[0]
                if incorrect_aggregate == True:
                    incorrect_aggregate_type = random.choices([1, 2], weights=[0.6, 0.4])[0]
                    if incorrect_aggregate_type == 1:
                        keyword_to_replace2 = [agg for agg in keywords_to_replace2 if agg in incorrect_query]
                        if len(keyword_to_replace2) != 0:
                            replacer_key = random.choice(keywords_to_replace2)
                            incorrect_query = incorrect_query.replace(keyword_to_replace2[0], replacer_key)
                            incorrect_query_split = incorrect_query.split(" ")
                    elif incorrect_aggregate_type == 2:
                        keyword_to_shift = [agg for agg in keywords_to_replace2 if agg in incorrect_query]
                        if len(keyword_to_shift) != 0:
                            incorrect_query_split[1] = keyword_to_shift[0] + f"({incorrect_query_split[1]})".replace(",", "") + ","
                            incorrect_query_split[2] = incorrect_query_split[2].replace(")", "").replace("(", "").replace(keyword_to_shift[0], "")
                            incorrect_query = ' '.join(incorrect_query_split)

                incorrect_operator = random.choices([True, False], weights=[0.7, 0.3])[0]
                if incorrect_operator == True:
                    operator_to_replace = [op for op in operators_to_replace if op in incorrect_query_split]
                    incorrect_operator_type = random.choice([1, 2])
                    if (incorrect_operator_type == 2) and (len(set(operator_to_replace)) != 1):
                        for i in range(len(incorrect_query_split)):
                            if incorrect_query_split[i] == operator_to_replace[0]:
                               incorrect_query_split[i] =  operator_to_replace[1]
                            elif incorrect_query_split[i] == operator_to_replace[1]:
                               incorrect_query_split[i] =  operator_to_replace[0]
                    else:
                        for operator in operators_to_replace:
                            replacer_operator = random.choice(operators_to_replace)
                            incorrect_query_split = [replacer_operator if element == operator else element for element in incorrect_query_split]
                            incorrect_query = ' '.join(incorrect_query_split)
                
                incorrect_query = incorrect_query.replace("GROUPBY", "GROUP BY")
                if (incorrect_query == random_query) or (incorrect_query in incorrect_querys):
                    continue
                
                incorrect_querys.append(incorrect_query)
                break
                
        task_from_query = ChatBot.get_task_from_query(random_query, columns_with_name_table) + \
            " Из предложенных 4 вариантов запросов выберите 1 который подходит под условия выборки."
        return [random_query, task_from_query, result, incorrect_querys]


