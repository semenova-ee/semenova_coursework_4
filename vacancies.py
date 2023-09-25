import re


class Vacancy:
    def __init__(self, id: int, name: str, url: str, salary_from: int, salary_to: int,
                 requirements: str, site: str) -> None:
        self._name = name
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._requirements = requirements
        self._id = id
        self.site = site

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if 5 < len(value) < 30:
            self._name = value
        else:
            raise ValueError("Имя должно быть от 5 до 30 символов в длину")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        """Простая проверка на валидность URL с использованием регулярного выражения"""
        url_pattern = r'^(https?://(?:www\.superjob\.ru/vakansii|hh\.ru/vacancy/\d+))$'
        if re.match(url_pattern, value):
            self._url = value
        else:
            raise ValueError("URL не является валидным")

    @property
    def requirements(self):
        return self._requirements

    @requirements.setter
    def requirements(self, value):
        """Проверка длины требований"""
        if len(value) >= 30:
            self._requirements = value
        else:
            raise ValueError("Требования должны содержать не менее 30 символов")

    @property
    def salary(self):
        """Получает среднее значение по заработной плате"""
        return (self._salary_from + self._salary_to) // 2

    def __eq__(self, other):
        # Реализация оператора ==
        return self.salary == other.salary

    def __lt__(self, other):
        # Реализация оператора <
        return self.salary < other.salary

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "requirements": self._requirements,
            "site": self.site
        }
