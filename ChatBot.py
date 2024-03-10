import g4f
import random 

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
                    model=g4f.models.gpt_35_long,
                    messages=[
                        {"role": "user", "content": f"{random_query}"},
                        {"role": "system", "content": "Инструкции: 1)Переведи запрос на русский человеческий язык. \
                            2)Нужно делать перевод запроса в стиле задания \"Выберите...\" \" \
                            3)Дополнительно в скобках () по мере текста укажи названия таблиц и полей таблиц на английском"}],
                    # proxy="http://160.153.0.19:80",
                    timeout=200,
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
            except Exception as ex:
                continue

        return response.replace("\"", "")
    

    




