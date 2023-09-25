import os
from abc import ABC, abstractmethod
import requests


class APIManager(ABC):
    url = ''
    headers = {}

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """Получает вакансии"""
        pass

    @staticmethod
    def format_data(d: dict) -> list:
        """Форматирует пришедшие по API данные"""
        pass


class HeadHunterAPI(APIManager):
    url = 'https://api.hh.ru/vacancies?per_page=50&text='
    headers = {'User-Agent': 'api-test-agent'}

    def get_vacancies(self, keyword: str) -> list:
        """Получает вакансии"""
        r = requests.get(self.url+keyword, headers=self.headers)
        return HeadHunterAPI.format_data(r.json()["items"])

    @staticmethod
    def inspect_salary_from(vacancy: dict) -> int or None:
        """Получает минимальную заработную плату"""
        if vacancy["salary"] is None:
            return None
        from_salary = vacancy["salary"]["from"]
        to_salary = vacancy["salary"]["to"]
        if vacancy['salary']['currency'] != "RUR":
            return None
        elif from_salary and to_salary:
            return int(from_salary)
        elif to_salary is None:
            return None
        elif from_salary is None:
            return None

    @staticmethod
    def inspect_salary_to(vacancy: dict) -> int or None:
        """Получает максимальную заработную плату"""
        if vacancy["salary"] is None:
            return None
        from_salary = vacancy["salary"]["from"]
        to_salary = vacancy["salary"]["to"]
        if vacancy['salary']['currency'] != "RUR":
            return None
        elif from_salary and to_salary:
            return int(to_salary)
        elif to_salary is None:
            return None
        elif from_salary is None:
            return None

    @staticmethod
    def format_data(vacancies: list) -> list:
        """Форматирует пришедшие по API данные"""
        inspected_vacancies = []
        for vacancy in vacancies:
            salary_from = HeadHunterAPI.inspect_salary_from(vacancy)
            salary_to = HeadHunterAPI.inspect_salary_to(vacancy)
            if salary_from and salary_to is not None:
                inspected_vacancy = {
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "url": vacancy["alternate_url"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "requirements": vacancy["snippet"]["requirement"],
                    "site": "HeadHunter"
                }
                inspected_vacancies.append(inspected_vacancy)
        return inspected_vacancies


class SuperJobAPI(APIManager):
    url = 'https://api.superjob.ru/2.0/vacancies/?count=50&keyword='
    headers = {'X-Api-App-Id': os.getenv("SUPERJOB_API_KEY").lstrip()}

    def get_vacancies(self, keyword: str) -> list:
        """Получает вакансии"""
        r = requests.get(self.url+keyword, headers=self.headers)
        return SuperJobAPI.format_data(r.json()["objects"])

    @staticmethod
    def inspect_salary_from(vacancy: dict) -> int or None:
        """Получает минимальную заработную плату"""
        from_salary = vacancy["payment_from"]
        to_salary = vacancy["payment_to"]
        if vacancy['currency'] != "rub":
            return None
        elif from_salary and to_salary:
            return int(from_salary)
        elif to_salary is None:
            return None
        elif from_salary is None:
            return None

    @staticmethod
    def inspect_salary_to(vacancy: dict) -> int or None:
        """Получает максимальную заработную плату"""
        from_salary = vacancy["payment_from"]
        to_salary = vacancy["payment_to"]
        if vacancy['currency'] != "rub":
            return None
        elif from_salary and to_salary:
            return int(to_salary)
        elif to_salary is None:
            return None
        elif from_salary is None:
            return None

    @staticmethod
    def format_data(vacancies: list) -> list:
        """Форматирует пришедшие по API данные"""
        inspected_vacancies = []
        for vacancy in vacancies:
            salary_from = SuperJobAPI.inspect_salary_from(vacancy)
            salary_to = SuperJobAPI.inspect_salary_to(vacancy)
            if salary_from and salary_to is not None:
                inspected_vacancy = {
                    "id": vacancy["id"],
                    "name": vacancy["profession"],
                    "url": vacancy["link"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "requirements": vacancy["candidat"],
                    "site": "SuperJob"
                }
                inspected_vacancies.append(inspected_vacancy)
        return inspected_vacancies
