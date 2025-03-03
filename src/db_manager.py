from unittest import result

import psycopg2
from psycopg2.extensions import connection
from typing import List, Dict, Any, Optional

class DBManager:
    """ Класс для управления базой данных PostgreSQL """

    def __init__(self, dsn: str) -> None:
        """ Инициализация соединения с базой данных """
        self.connection = psycopg2.connect(dsn)
        self.connection.autocommit = True

    def create_tables(self) -> None:
        """ Создает таблицы организаций и вакансий """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    employer_id INTEGER UNIQUE,
                    name TEXT NOT NULL,
                );
            """)
            # Создание таблицы вакансий с внешним ключом на компании
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER REFERENCES companies(id),
                    title TEXT NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url TEXT
                );
                """)

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """ Возвращает список всех компаний и количество вакансий для данной """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, COUNT(v.id) as vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.id;
            """)
            result = cursor.fetchall()
        return [{"company": row[0], "vacancies_count": row[1]} for row in result]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """ Возвращает список ввсех вакансий с указанием компании, названия вакансии, зарплаты и URL """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id;
            """)
            result = cursor.fetchall()
        return [
            {"company": row[0], "title": row[1], "salary_from": row[2], "salary_to": row[3], "url": row[4]}
            for row in result
        ]

    def get_avg_salary(self) -> Optional[float]:
        """ Вычисляет среднюю зарплату по вакансиям """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG((salary_from + salary_to) / 2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)
            result = cursor.fetchone()
        return result[0] if result and result[0] is not None else None

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """ Возвращает список вакансий, у которых зарплата выше средней по всем вакансиям """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE ((salary_from + salary_to) / 2.0) > %s;
            """, (avg_salary,))
            result = cursor.fetchall()
        return [
            {"company": row[0], "title": row[1], "salary_from": row[2], "salary_to": row[3], "url": row[4]}
            for row in result
        ]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """ Возвращает список вакансий по ключевому слову """
        pattern = f"%{keyword}%"
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.title ILIKE %s;
            """, (pattern,))
            result = cursor.fetchall()
        return [
            {"company": row[0], "title": row[1], "salary_from": row[2], "salary_to": row[3], "url": row[4]}
            for row in result
        ]

    def close(self) -> None:
        """ Закрытие соединения с базой данных """
        self.connection.close()
