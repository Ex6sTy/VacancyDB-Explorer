import psycopg2
from config import config


def create_database(database_name: str):
    conn = psycopg2.connect(dbname="postgres", **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()


def create_tables(database_name: str):
    conn = psycopg2.connect(dbname=database_name, **config())
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                url VARCHAR(255)
            )
        """
        )
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                url VARCHAR(255)
            )
        """
        )
    conn.commit()
    conn.close()
