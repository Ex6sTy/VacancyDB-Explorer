import pytest
from src.api import get_employer_data, get_vacancies_data

def test_get_employer_data():
    # Проверяем, что функция возвращает данные для существующего работодателя
    employer_id = '15478'  # Пример ID работодателя (Ростелеком)
    data = get_employer_data(employer_id)
    assert data is not None
    assert 'name' in data
    assert 'description' in data
    assert 'site_url' in data

def test_get_vacancies_data():
    # Проверяем, что функция возвращает данные о вакансиях
    employer_id = '15478'  # Пример ID работодателя (Ростелеком)
    data = get_vacancies_data(employer_id)
    assert data is not None
    assert isinstance(data, list)
    if len(data) > 0:
        assert 'name' in data[0]  # Название вакансии
        assert 'salary' in data[0]  # Зарплата