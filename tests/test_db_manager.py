import os
import pytest
from src.db_manager import DBManager

# DSN для тестовой базы данных. Лучше создать специальную тестовую БД.
TEST_DSN = os.getenv("TEST_DATABASE_URL", "dbname=test_vacancy_db user=postgres password=secret host=localhost")


@pytest.fixture(scope="module")
def db_manager():
    """
    Фикстура для создания и очистки тестовой базы данных.
    """
    db = DBManager(TEST_DSN)
    db.create_tables()
    yield db
    # Очистка тестовой БД: удаляем таблицы
    with db.connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS vacancies;")
        cursor.execute("DROP TABLE IF EXISTS companies;")
    db.close()


def test_insert_and_get_companies(db_manager):
    """
    Тестирует вставку компании и последующий запрос количества вакансий.
    """
    # Вставляем тестовую компанию
    with db_manager.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO companies (employer_id, name)
            VALUES (%s, %s)
            RETURNING id;
        """, (999, "Test Company"))
        company_id = cursor.fetchone()[0]

    # Убеждаемся, что компания добавлена и вакансий для нее нет
    companies = db_manager.get_companies_and_vacancies_count()
    test_company = next((comp for comp in companies if comp["company"] == "Test Company"), None)
    assert test_company is not None, "Компания не найдена в базе данных"
    assert test_company["vacancies_count"] == 0, "Количество вакансий должно быть 0"


def test_avg_salary_with_no_vacancies(db_manager):
    """
    Тестирует вычисление средней зарплаты, когда вакансий нет.
    """
    avg_salary = db_manager.get_avg_salary()
    assert avg_salary is None, "Средняя зарплата должна быть None, когда вакансий нет"

# Можно добавить и другие тесты, например, для вставки вакансий и запроса вакансий с фильтрацией.
