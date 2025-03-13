import pytest
import psycopg2
from src.database import create_database, create_tables
from config import config

@pytest.fixture
def test_db_name():
    return "test_hh_vacancies"

def test_create_database(test_db_name):
    # Проверяем создание базы данных
    create_database(test_db_name)
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
    assert cur.fetchone() is not None
    cur.close()
    conn.close()

def test_create_tables(test_db_name):
    # Проверяем создание таблиц
    create_tables(test_db_name)
    conn = psycopg2.connect(dbname=test_db_name, **config())
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    table_names = [table[0] for table in tables]
    assert 'employers' in table_names
    assert 'vacancies' in table_names
    cur.close()
    conn.close()