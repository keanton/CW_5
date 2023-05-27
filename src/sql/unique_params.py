import psycopg2
from src.auth_data import user, password


def create_params(database_name: str):
    """
    Функция защиты от дублей в таблице
    :param database_name:
    :return:
    """
    conn = psycopg2.connect(host="localhost", database=database_name, user=user, password=password)    #connect to db подключение к бд
    try:
        with conn:
            with conn.cursor() as cur:    #create cursor
                cur.execute(
                    """
                    CREATE UNIQUE INDEX idx_emp_name ON employers (name);
                    """
                )     #Защита от дублей в таблице

                cur.execute(
                    """
                    CREATE UNIQUE INDEX idx_vacancies_url ON vacancies (vac_url);
                    """
                )    #Защита от дублей в таблице
    finally:
        conn.close()    #close connection to db закрываем соединение