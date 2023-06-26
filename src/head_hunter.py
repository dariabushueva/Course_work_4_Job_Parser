import requests
import time
from src.api_vacancy import ApiVacancy
from src.exeptions import ParsingError


class HeadHunter(ApiVacancy):
    """Класс для работы с API сайта hh.ru"""

    URL_HH_VACANCY = 'https://api.hh.ru/vacancies'
    SLEEP_TIME = 0.25

    def __init__(self, vacancy):

        self.headers = {
            "User-Agent": "MyApp / 1.0(my - app - feedback @ example.com)"
        }

        self.params = {
                'text': vacancy,  # Текст фильтра
                'area': 113,  # Поиск осуществляется по вакансиям России - 113 (город фильтруется ключевым словом)
                'page': None,
                'per_page': 100,  # Кол-во вакансий на 1 странице
                'archived': False  # Не включать архивные вакансии
        }

        self.vacancies = []

    def get_request(self):
        """ Создание запроса на сайт HH.ru """

        response = requests.get(self.URL_HH_VACANCY, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных {response.status_code}")
        data = response.json()
        return data

    def get_vacancies(self, pages_amount=20):
        """ Получение списка вакансий с сайта HH.ru """

        self.vacancies.clear()

        for page in range(0, pages_amount):
            self.params['page'] = page
            try:
                page_vacancies = self.get_request()["items"]
                print(f"({self.__class__.__name__}) Загружаю {page + 1} страницу с вакансиями")
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
            if (self.get_request()['pages'] - page) <= 1:  # Проверка на последнюю страницу, если вакансий меньше 2000
                break
            time.sleep(self.SLEEP_TIME)

    def generalization(self):
        """ Приведение вакансий к общему виду """

        general_vacancies = []
        for vacancy in self.vacancies:
            general_vacancy = {
                "title": vacancy['name'],
                "employer": vacancy["employer"]["name"],
                "url": vacancy["alternate_url"],
                "description": vacancy["snippet"]["responsibility"]
            }
            salary = vacancy["salary"]
            if salary:
                general_vacancy["salary_from"] = salary["from"]
                general_vacancy["salary_to"] = salary["to"]
                general_vacancy["currency"] = salary["currency"]
            else:
                general_vacancy["salary_from"] = None
                general_vacancy["salary_to"] = None
                general_vacancy["currency"] = None

            general_vacancies.append(general_vacancy)

        return general_vacancies

