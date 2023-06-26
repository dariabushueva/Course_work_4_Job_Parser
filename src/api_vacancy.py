from abc import ABC, abstractmethod


class ApiVacancy(ABC):
    """Класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass





