import psycopg2
from src.api import get_employer_data, get_vacancies_data
from config import config


def fill_employers_table(database_name: str, employer_ids: list):
    conn = psycopg2.connect(dbname=database_name, **config())
    with conn.cursor() as cur:
        for employer_id in employer_ids:
            employer_data = get_employer_data(employer_id)
            if employer_data:
                cur.execute(
                    """
                    INSERT INTO employers (name, description, url)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                """,
                    (
                        employer_data["name"],
                        employer_data["description"],
                        employer_data["site_url"],
                    ),
                )
                employer_id = cur.fetchone()[0]
                vacancies_data = get_vacancies_data(employer_id)
                if vacancies_data:
                    for vacancy in vacancies_data:
                        salary_from = (
                            vacancy["salary"]["from"] if vacancy["salary"] else None
                        )
                        salary_to = (
                            vacancy["salary"]["to"] if vacancy["salary"] else None
                        )
                        cur.execute(
                            """
                            INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url)
                            VALUES (%s, %s, %s, %s, %s)
                        """,
                            (
                                employer_id,
                                vacancy["name"],
                                salary_from,
                                salary_to,
                                vacancy["alternate_url"],
                            ),
                        )
    conn.commit()
    conn.close()
