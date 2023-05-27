from src.auth_data import user, password

import psycopg2


def create_db(database_name: str):
    """
    Создание базы данных и таблиц для сохранения данных
    """
    try:
        conn = psycopg2.connect(dbname='postgres', user=user, password=password)    #connect to db подключение к бд
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {database_name}")
    except psycopg2.errors.DuplicateDatabase:
        print('ОШИБКА:  база данных "sky" уже существует')
    finally:
        conn.close()

    conn = psycopg2.connect(host="localhost", database=database_name, user=user, password=password)
    try:
        with conn:
            with conn.cursor() as cur:    #create cursor
                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        emp_address VARCHAR(50),
                        emp_url VARCHAR(255)
                    )
                    """
                )    # Создание таблицы работодателей

                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        name VARCHAR NOT NULL,
                        area VARCHAR(50) NOT NULL,
                        vac_url VARCHAR(255),
                        description TEXT,
                        salary_from INTEGER,
                        salary_to INTEGER
                    )
                    """
                )     # Создание таблицы вакансий
    finally:
        conn.close()    #close connection to db закрываем соединение