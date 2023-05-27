from src.auth_data import user, password

import psycopg2


class DBManager:
    """Класс работы с БД"""
    def __init__(self, database_name:str):
        self._database = database_name

    def get_companies_and_vacancies_count(self):
        """
        Функция получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        conn = psycopg2.connect(host="localhost", database=self._database, user=user, password=password)
        cur = conn.cursor()
        cur.execute("select employers.name, count(*) from vacancies\nJOIN employers ON employers.employer_id = vacancies.employer_id\ngroup by employers.employer_id")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}: {row[1]} vacancies")
        cur.close()
        conn.close()

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        conn = psycopg2.connect(host="localhost", database=self._database, user=user, password=password)
        cur = conn.cursor()
        cur.execute(
            "SELECT employers.name AS employer_name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.vac_url\nFROM vacancies\nJOIN employers\nON vacancies.employer_id = employers.employer_id;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям.
        :return:
        """
        conn = psycopg2.connect(host="localhost", database=self._database, user=user, password=password)
        cur = conn.cursor()
        cur.execute("select round(avg(salary_from)) from vacancies")
        rows = cur.fetchall()
        print(f"Среднее значение 'зарплаты от': {rows}")
        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        conn = psycopg2.connect(host="localhost", database=self._database, user=user, password=password)
        cur = conn.cursor()
        cur.execute("SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")
        rows = cur.fetchall()
        for row in rows:
         print(f"id: {row[0]} Вакансия: {row[2], row[3], row[4], row[5], row[6]}")
        cur.close()
        conn.close()

    def get_vacancies_with_keyword(self, user_input):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        :param user_input:
        :return:
        """
        conn = psycopg2.connect(host="localhost", database=self._database, user=user, password=password)
        cur = conn.cursor()
        sql_query = "SELECT * FROM vacancies WHERE name LIKE %s"    # Формируем SQL запрос
        search_params = (f'%{user_input}%',)    #Задаем параметры поиска
        cur.execute(sql_query, search_params)    # Выполняем запрос с параметрам
        result = cur.fetchall()
        for row in result:
            print(f"id: {row[0]} Вакансия: {row[2], row[3], row[4], row[5], row[6]}")
        cur.close()
        conn.close()
