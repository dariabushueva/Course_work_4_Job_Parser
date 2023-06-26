from abc import ABC, abstractmethod


class Saver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def read_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self, exception):
        pass
