import json
import os
from src.saver import Saver
from src.utils import currency_coefficient
from src.vacancy import Vacancy

DATA_JSON = os.path.join("data", "job.json")


class JSONSaver(Saver):
    """ Сохранение и работа с вакансиями через JSON """

    def __init__(self, data_json):
        self.add_vacancy(data_json)

    def add_vacancy(self, data_json):
        """ Создание JSON-файла с вакансиями """

        with open(DATA_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, indent=4, ensure_ascii=False)

    def read_vacancy(self):
        """ Чтение вакансий из файла"""

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)

        return [Vacancy(i) for i in data_vacancies]

    def get_vacancies_by_salary(self, salary):
        """ Поиск вакансий по зарплате """

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)
            vacancies_by_salary = []
            for vacancy in data_vacancies:
                if vacancy["salary_to"]:
                    if vacancy["currency"] == "RUR" and vacancy["salary_to"] > salary:
                        vacancies_by_salary.append(vacancy)
                    if vacancy["currency"] == "EUR" and vacancy["salary_to"] > (salary / currency_coefficient('EUR')):
                        vacancies_by_salary.append(vacancy)
                    if vacancy["currency"] == "USD" and vacancy["salary_to"] > (salary / currency_coefficient('USD')):
                        vacancies_by_salary.append(vacancy)

        return [Vacancy(i) for i in vacancies_by_salary]

    def delete_vacancy(self, exception):
        """ Удаление вакансий по слову-исключению """

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)
            new_vacancies = []
            for vacancy in data_vacancies:
                if exception.casefold() not in vacancy["title"].casefold():
                    new_vacancies.append(vacancy)

        return [Vacancy(i) for i in new_vacancies]
