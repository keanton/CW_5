from abc import ABC, abstractmethod
import requests


class Engine(ABC):
    def __init__(self, search_query: str) -> None:
        self.search_query = search_query
        self.per_page = 100
        self._employer_id = None
        self._employer_one = None
        self._vacancies_for_employer = None

    @abstractmethod
    def get_requests(self):
        pass

    class HH(Engine):
        def __init__(self, search_query: str):
            super().__init__(search_query)
            self.data = []
            self.url = "https://api.hh.ru/vacancies/"
            self.params = {"text", self._search_query, "per_page": self._per_page}

        def get_request(self)-> list:
            responce =requests.get(self.url, self.params) #отправка запроса к api
            if responce.status_code == 200:
                vacancies = responce.json()["items"]
                for vacancy in vacancies:
                    if vacancy['employer']['name'] == self.search_query
                        self._employer_id = vacancy['employer']['id']
                        self._employer_one = {'id': vacancy['employer']['id'], 'name': vacancy['employer']['name'],
                                                 'address': vacancy['address'], 'emp_url': vacancy['employer']['url']}

            else:
                print("Error:", responce.status_code)

            url = f"https://api.hh.ru/vacancies?employer_id={self._employer_id}"    # URL запроса к API
            response = requests.get(url, self.params)  # Отправка запроса к API
            if response.status_code == 200:  # Обработка ответа от API
                vacancies = response.json()['items']  # Извлечение списка вакансий из ответа
                self._vacancies_for_employer = []  # Список вакансий по одному айди-работодателя
                for vacancy in vacancies:
                    if vacancy['salary'] is not None:
                        vac_data = {'name': vacancy['name'], 'area': vacancy['area']['name'], 'url': vacancy['url'],
                                    'description': vacancy['snippet']['requirement'],
                                    'payment_from': vacancy['salary']['from'], 'payment_to': vacancy['salary']['to']}
                        self._vacancies_for_employer.append(vac_data)
                    else:
                        continue
            else:
                print(f'Ошибка запроса: {response.status_code}')
            self.data.append({
                'employer': self._employer_one,
                'vacancies': self._vacancies_for_employer
            })
            return self.data
