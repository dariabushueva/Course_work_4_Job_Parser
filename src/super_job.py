import requests
import time
from src.api_vacancy import ApiVacancy
from src.exeptions import ParsingError


class SuperJob(ApiVacancy):
    """Класс для работы с API сайта SuperJob.ru"""

    URL_SJ_VACANCY = 'https://api.superjob.ru/2.0/vacancies/'
    SLEEP_TIME = 0.5

    def __init__(self, vacancy):

        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": "v3.r.137604708.4625e11082f169e37b34e82326c54d5f8246fda6.1d5ab90621c5c13d3650f5b8eb40e2cca239d3e0",
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.params = {
            'keyword': vacancy,  # Ключевое слово для поиска вакансий
            'town': 0,  # Поиск осуществляется по вакансиям России - 113 (город фильтруется ключевым словом)
            'count': 100,  # Количество результатов
            'page': None,
            'archived': False
        }

        self.vacancies = []

    def get_request(self):
        """ Создание запроса на сайт SuperJob.ru """

        response = requests.get(self.URL_SJ_VACANCY, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных {response.status_code}")
        data = response.json()
        return data

    def get_vacancies(self, pages_amount=20):
        """ Получение списка вакансий с сайта SuperJob.ru """

        self.vacancies.clear()

        for page in range(0, pages_amount):
            self.params['page'] = page
            try:
                page_vacancies = self.get_request()["objects"]
                print(f"({self.__class__.__name__}) Загружаю {page + 1} страницу с вакансиями")
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
            if not self.get_request()['more']:  # Проверка на "есть ли ещё результаты", если вакансий меньше 2000
                break
            time.sleep(self.SLEEP_TIME)

    def generalization(self):
        """ Приведение вакансий к общему виду """

        general_vacancies = []
        for vacancy in self.vacancies:
            general_vacancy = {
                "title": vacancy["profession"],
                "employer": vacancy["firm_name"],
                "url": vacancy["link"],
                "description": vacancy["candidat"],
                "salary_from": vacancy["payment_from"],
                "salary_to": vacancy["payment_to"],
                "currency": vacancy["currency"]
            }

            general_vacancies.append(general_vacancy)

        return general_vacancies
