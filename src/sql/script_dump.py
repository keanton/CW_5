from src.auth_data import user, password

import psycopg2

def dump_db(hh_vacancies, database_name):
    conn = psycopg2.connect(host="localhost", database=database_name, user=user, password=password)    #Установка соединения с БД
    try:
        with conn:
            with conn.cursor() as cur:  # create cursor
                for employer in hh_vacancies:
                    if employer['employer'] is not None:
                        if len(employer) > 1:
                            #print(employer['employer'])
                            employer_data = employer['employer']
                            if employer_data['address'] is not None:
                                cur.execute(
                                    """
                                    INSERT INTO employers (name, emp_address, emp_url)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (name) DO UPDATE    
                                    SET emp_address = EXCLUDED.emp_address
                                    RETURNING employer_id
                                    """,
                                    (employer_data['name'], employer_data['address']['city'], employer_data['emp_url'])
                                )    #Добавление данных о работодателях
                            else:
                                cur.execute(
                                    """
                                    INSERT INTO employers (name, emp_address, emp_url)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (name) DO UPDATE    
                                    SET emp_address = EXCLUDED.emp_address
                                    RETURNING employer_id
                                    """,
                                    (employer_data['name'], employer_data['address'], employer_data['emp_url'])
                                )    #Добавление данных о работодателях

                            employer_id = cur.fetchone()[0]
                            vacancies_data = employer['vacancies']
                            for vacancy in vacancies_data:
                                cur.execute(
                                    """
                                    INSERT INTO vacancies (employer_id, name, area, vac_url, description, salary_from, salary_to)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (vac_url) DO UPDATE    
                                    SET description = EXCLUDED.description
                                    """,
                                    (employer_id, vacancy['name'], vacancy['area'], vacancy['url'],
                                     vacancy['description'], vacancy['payment_from'], vacancy['payment_to'])
                                )    # Добавление данных о вакансиях

    finally:
        conn.close()  # close connection to db закрываем соединение