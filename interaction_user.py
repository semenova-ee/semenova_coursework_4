from api import HeadHunterAPI, SuperJobAPI
from vacancies import Vacancy
from json_manager import JsonManager


json_work = JsonManager('vacancies.json')

sites_info = """
Выберите с каких сайтов вы хотите получить вакансии:
1 -- Headhunter.ru 
2 -- Superjob.ru
3 -- Oба сайта
"""


def filter_vacancies(site: int, keywords: list, salary: str):
    """Выводит отфильтрованные вакансии"""
    filtered_vacancies = []
    if site == 1:
        filtered_vacancies.extend(json_work.get_vacancies_by_salary(salary, "HeadHunter"))
        for keyword in keywords:
            filtered_vacancies.extend(json_work.get_vacancies_by_keyword(keyword, "HeadHunter"))
    elif site == 2:
        filtered_vacancies.extend(json_work.get_vacancies_by_salary(salary, "SuperJob"))
        for keyword in keywords:
            filtered_vacancies.extend(json_work.get_vacancies_by_keyword(keyword, "SuperJob"))
    else:
        filtered_vacancies.extend(json_work.get_vacancies_by_salary(salary, "HeadHunter"))
        for keyword in keywords:
            filtered_vacancies.extend(json_work.get_vacancies_by_keyword(keyword, "HeadHunter"))
        filtered_vacancies.extend(json_work.get_vacancies_by_salary(salary, "SuperJob"))
        for keyword in keywords:
            filtered_vacancies.extend(json_work.get_vacancies_by_keyword(keyword, "SuperJob"))
    return filtered_vacancies


def get_vacancies_from_sites(platforms: int, keyword: str):
    """Получает вакансии с сайта"""
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(keyword)
    sp_api = SuperJobAPI()
    sp_vacancies = sp_api.get_vacancies(keyword)
    if platforms == 1:
        for v in hh_vacancies:
            vac = Vacancy(*v.values())
            json_work.add_vacancy(vac)
    elif platforms == 2:
        for v in sp_vacancies:
            vac = Vacancy(*v.values())
            json_work.add_vacancy(vac)
    else:
        for hh_vacancy in hh_vacancies:
            vac = Vacancy(*hh_vacancy.values())
            json_work.add_vacancy(vac)
        for sp_vacancy in sp_vacancies:
            vac = Vacancy(*sp_vacancy.values())
            json_work.add_vacancy(vac)


def user_interaction():
    """Получает от пользователя информацию, необходимую для фильтрации сайтов и вывода информации"""
    print(sites_info)
    while True:
        try:
            platforms = int(input("С каких сайтов хотите получить вакансии? "))
            if platforms < 1 or platforms > 3:
                raise ValueError("Введите число от 1 до 3")
            break
        except ValueError:
            print("Некорректный ввод. Введите число от 1 до 3.")

    search_query = input("Введите ваш поисковый запрос (Например 'Python'): ")
    get_vacancies_from_sites(platforms, search_query)

    while True:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            if top_n <= 0:
                raise ValueError("Введите положительное число.")
            break
        except ValueError:
            print("Некорректный ввод. Введите положительное число.")

    filter_words = input("Введите ключевые слова для фильтрации вакансий (например, Junior): ").split()

    while True:
        desired_salary = input("Введите желаемую зарплату (или 'stop' для завершения): ")
        if desired_salary.lower() == 'stop':
            break
        try:
            # You can add more specific validation for the salary input if needed
            if not desired_salary.isdigit():
                raise ValueError("Введите число или 'stop' для завершения.")
            break
        except ValueError:
            print("Некорректный ввод. Введите число или 'stop' для завершения.")
    filtered_vacancies = filter_vacancies(platforms, filter_words, desired_salary)
    return filtered_vacancies, top_n


vacancies, top_n = user_interaction()

vacancy_top = []
for vacancy in vacancies[:top_n]:
    if vacancy not in vacancy_top:
        vacancy_top.append(vacancy)
vacancy_top_sorted = sorted(vacancy_top, key=lambda x: x['salary_from'], reverse=True)

for vacancy in vacancy_top_sorted:
    print(f" Вакансия {vacancy['name']}, {vacancy['url']}:\n"
          f" зарабатная плата от {vacancy['salary_from']} руб. до {vacancy['salary_to']} руб.\n"
          f" требования {vacancy['requirements']}\n"
          f" сайт {vacancy['site']}\n"
          f"_____________________\n")
