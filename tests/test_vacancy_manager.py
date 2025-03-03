import pytest
from src.vacancy_manager import parse_vacancy, process_vacancies, filter_vacancies_by_keyword

def test_parse_vacancy_with_salary():
    vacancy_data = {
        "name": "Software Engineer",
        "alternate_url": "http://example.com/vacancy/1",
        "salary": {"from": 1000, "to": 2000}
    }
    expected = {
        "title": "Software Engineer",
        "salary_from": 1000,
        "salary_to": 2000,
        "url": "http://example.com/vacancy/1"
    }
    assert parse_vacancy(vacancy_data) == expected

def test_parse_vacancy_without_salary():
    vacancy_data = {
        "name": "Data Scientist",
        "alternate_url": "http://example.com/vacancy/2",
        "salary": None
    }
    expected = {
        "title": "Data Scientist",
        "salary_from": None,
        "salary_to": None,
        "url": "http://example.com/vacancy/2"
    }
    assert parse_vacancy(vacancy_data) == expected

def test_filter_vacancies_by_keyword():
    vacancies = [
        {"title": "Python Developer", "salary_from": 1200, "salary_to": 2200, "url": "http://example.com/vacancy/3"},
        {"title": "Java Developer", "salary_from": 1100, "salary_to": 2100, "url": "http://example.com/vacancy/4"}
    ]
    filtered = filter_vacancies_by_keyword(vacancies, "python")
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Python Developer"
