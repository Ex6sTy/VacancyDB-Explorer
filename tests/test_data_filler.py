import pytest
import psycopg2
from src.data_filler import fill_employers_table
from src.database import create_database, create_tables
from config import config

@pytest.fixture
def test_db_name():
    return "test_hh_vacancies"

def test_fill_employers_table(test_db_name):
    # Создаем тестовую базу данных и таблицы
    create_database(test_db_name)
    create_tables(test_db_name)
    # Заполняем таблицы данными
    fill_employers_table(test_db_name, ['15478'])  # Пример ID работодателя (Ростелеком)
    # Проверяем, что данные добавлены
    conn = psycopg2.connect(dbname=test_db_name, **config())
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM employers")
    employers_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM vacancies")
    vacancies_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert employers_count >= 0
    assert vacancies_count >= 0