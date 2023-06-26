from src.json_saver import JSONSaver
from src.head_hunter import HeadHunter
from src.super_job import SuperJob
from src.vacancy import Vacancy


def main():

    select_site = int(input("Введите на каком сайте будем искать вакансии:\n"
                        "1 - HeadHanter.ru,\n"
                        "2 - SuperJob.ru\n"))

    select_vacancy = "python"  # input("Введите название вакансии: \n")
    select_city = "Москва"  # input("Введите город поиска: \n")
    select_pages = 1  # int(input("Введите количество страниц поиска\n"))

    vacancies_json = []

    if select_site == 1:

        hh = HeadHunter(select_vacancy+select_city)
        hh.get_vacancies(select_pages)
        vacancies_json.extend(hh.generalization())
        json_saver = JSONSaver(vacancies_json)
        all_vacancies = json_saver.read_vacancy()

    #    vacancies_json.clear()
    #    select_salary = int(input("Введите желаемую зп\n:"))
    #    salary = json_saver.get_vacancies_by_salary(select_salary)
    #    vacancies_json.extend(salary)
    #    print(vacancies_json)

    #    select_exception = input("Введите слово исключение для удаления ненужных вакансий:\n")
    #    del_v = json_saver.delete_vacancy(select_exception)
    #    vacancies_json.extend(del_v)
    #    print(vacancies_json)

    elif select_site == 2:

        sj = SuperJob(select_vacancy)
        sj.get_vacancies(select_pages)
        vacancies_json.extend(sj.generalization())
        json_saver = JSONSaver(vacancies_json)
        all_vacancies = json_saver.read_vacancy()

    for vacancy in all_vacancies:
        print(vacancy, end='\n')



if __name__ == "__main__":
    main()