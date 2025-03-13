import pytest
from src.db_manager import DBManager
from src.database import create_database, create_tables
from src.data_filler import fill_employers_table
from config import config

@pytest.fixture
def test_db_name():
    return "test_hh_vacancies"

@pytest.fixture
def db_manager(test_db_name):
    # Создаем тестовую базу данных и заполняем её данными
    create_database(test_db_name)
    create_tables(test_db_name)
    fill_employers_table(test_db_name, ['15478'])  # Пример ID работодателя (Ростелеком)
    return DBManager(test_db_name)

def test_get_companies_and_vacancies_count(db_manager):
    result = db_manager.get_companies_and_vacancies_count()
    assert isinstance(result, list)
    if len(result) > 0:
        assert isinstance(result[0], tuple)
        assert len(result[0]) == 2

def test_get_all_vacancies(db_manager):
    result = db_manager.get_all_vacancies()
    assert isinstance(result, list)
    if len(result) > 0:
        assert isinstance(result[0], tuple)
        assert len(result[0]) == 5

def test_get_avg_salary(db_manager):
    result = db_manager.get_avg_salary()
    assert result is None or isinstance(result, float)

def test_get_vacancies_with_higher_salary(db_manager):
    result = db_manager.get_vacancies_with_higher_salary()
    assert isinstance(result, list)

def test_get_vacancies_with_keyword(db_manager):
    result = db_manager.get_vacancies_with_keyword("менеджер")
    assert isinstance(result, list)

def test_get_vacancies_by_salary_and_keyword(db_manager):
    result = db_manager.get_vacancies_by_salary_and_keyword(50000, "менеджер")
    assert isinstance(result, list)