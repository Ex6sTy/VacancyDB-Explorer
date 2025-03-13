import psycopg2
from config import config
from typing import List, Tuple, Optional

class DBManager:
    """Класс для управления базой данных PostgreSQL."""

    def __init__(self, database_name: str) -> None:
        """
        Инициализирует объект DBManager.

        :param database_name: Имя базы данных для подключения.
        """
        self.conn = psycopg2.connect(dbname=database_name, **config())

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        :return: Список кортежей вида (название компании, количество вакансий).
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, COUNT(vacancies.vacancy_id)
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

        :return: Список кортежей вида (название компании, название вакансии, зарплата от, зарплата до, ссылка на вакансию).
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получает среднюю зарплату по всем вакансиям.

        :return: Средняя зарплата (float) или None, если данные отсутствуют.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            result = cur.fetchone()[0]
            return result if result is not None else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return: Список кортежей с информацией о вакансиях.
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                WHERE (salary_from + salary_to) / 2 > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

        :param keyword: Ключевое слово для поиска в названиях вакансий.
        :return: Список кортежей с информацией о вакансиях.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                WHERE title ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()

    def get_vacancies_by_salary_and_keyword(self, salary: int, keyword: str) -> List[Tuple]:
        """
        Получает список вакансий, у которых зарплата выше или равна указанной,
        и в названии которых содержится ключевое слово.

        :param salary: Минимальная желаемая зарплата.
        :param keyword: Ключевое слово для поиска в названиях вакансий.
        :return: Список кортежей с информацией о вакансиях.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE (vacancies.salary_from >= %s OR vacancies.salary_to >= %s)
                AND vacancies.title ILIKE %s
            """, (salary, salary, f'%{keyword}%'))
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.conn.close()