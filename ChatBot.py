import os
from dotenv import load_dotenv
import g4f
from g4f.errors import RetryProviderError

load_dotenv()

model = os.getenv("MODEL")
proxy = os.getenv("PROXY")

print(f"{proxy = }")

class ChatBot:
    def __init__(self):
        ChatBot.g4f.debug.logging = False  
        ChatBot.g4f.check_version = False  
        ChatBot.proxy_servers = ["http://160.153.0.19:80"]
     
    @staticmethod
    def get_task_from_query(random_query, columns_with_name_table):
        columns_with_name_table.sort(key = len, reverse = True)
        while True:
            try:    
                response = g4f.ChatCompletion.create(
                    messages=[
                        {"role": "user", "content": f"{random_query}"},
                        {"role": "system", "content": "Инструкции: 1)Переведи запрос на русский человеческий язык. \
                            2)Нужно делать перевод запроса в стиле задания \"Выберите...\" \" \
                            3)Дополнительно в скобках () по мере текста укажи названия таблиц и полей таблиц на английском"}],
                    timeout = 200,
                    model=model,
                    proxy=proxy
                )
                
                response_check = response
                checker = True
                for attribute in columns_with_name_table:
                    if (attribute not in response_check):
                        checker = False
                        break
                    else:
                        response_check = response_check.replace(attribute, "")
                if checker == False:
                    continue
                
                if ("SELECT" not in response):
                    break
                else:
                    continue

                break
            except RetryProviderError as e:
                print(e)

        return response.replace("\"", "")
    

if __name__ == "__main__":
    from DatabaseConnector import Database
    from QueryGenerator import QueryGenerator

    db = Database("dbs/Book.db")
    gen = QueryGenerator(db)
    query = gen.generate_random_query()
    columns = gen.columns_with_name_table
    print(ChatBot.get_task_from_query(query, columns))