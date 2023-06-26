
class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy):
        self.title = vacancy["title"]
        self.employer = vacancy["employer"]
        self.url = vacancy["url"]
        self.description = vacancy["description"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]

    def __str__(self):

        return f"Название вакансии: {self.title}\n" \
               f"Работодатель: {self.employer}\n" \
               f"Ссылка: {self.url}\n" \
               f"Описание: {self.description}\n" \
               f"Валюта: {self.currency}\n" \
               f"Зарплата от: {self.salary_from}\n" \
               f"Зарплата до: {self.salary_to}\n" \
               f"{'-' * 30}\n"












