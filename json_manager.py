from abc import ABC, abstractmethod
import json
from json import JSONDecodeError


class VacancyManager(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary_range, site) -> list:
        pass

    @abstractmethod
    def get_vacancies_by_keyword(self, keyword, site) -> list:
        pass

    @abstractmethod
    def get_vacancy_by_site(self, site: str) -> list:
        pass

    @abstractmethod
    def delete_vacancy_by_id(self, id: int):
        pass


class JsonManager(VacancyManager):
    def __init__(self, filename):
        self.filename = filename
        self.vacancies = self._load_data()

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в список"""
        self.vacancies["items"].append(vacancy.to_dict())
        self._save_data()

    def get_vacancies_by_keyword(self, keyword, site):
        """Выводит отсортированный список вакансий по ключу"""
        matching_vacancies = []
        for vacancy in self.get_vacancy_by_site(site):
            if keyword in vacancy["name"]:
                matching_vacancies.append(vacancy)

        return matching_vacancies

    def get_vacancy_by_site(self, site: str) -> list:
        """Выводит отсортированный список вакансий по сайту"""
        matching_vacancies = []
        for vacancy in self.vacancies["items"]:
            if site == vacancy["site"]:
                matching_vacancies.append(vacancy)

        return matching_vacancies

    def _load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if data is not None:
                    return data
                else:
                    return {"items": []}
        except FileNotFoundError:
            return {"items": []}
        except JSONDecodeError:
            return {"items": []}

    def _save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=2)

    def get_vacancies_by_salary(self, salary, site):
        """Возвращает список отсортированных по зп вакансий"""
        matching_vacancies = []
        for vacancy in self.get_vacancy_by_site(site):
            if int(vacancy["salary_from"]) <= int(salary) <= int(vacancy["salary_to"]):
                matching_vacancies.append(vacancy)

        return matching_vacancies

    def get_vacancy_by_id(self, id: int):
        """Возвращает вакансию по id"""
        for vacancy in self.vacancies:
            if id == vacancy[id]:
                return vacancy[id]

    def delete_vacancy_by_id(self, id: int):
        """Удаляет вакансию по id"""
        self.vacancies["items"] = [v for v in self.vacancies["items"] if v["id"] != id]
        self._save_data()
