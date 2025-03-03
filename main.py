import os
from src.db_manager import DBManager
from src import api
from src import vacancy_manager


# Получение DSN для подключения к PostgreSQL из переменной окружения или использование дефолтного значения
DSN = os.getenv('DARABASE_URL', "dbname=vacancy_db user=postgres password=secret host=localhost")

def insert_company(db: DBManager, employer_id: int, name:str) -> int:
    """ Добавление записи компании в таблицу companies
    Если запись существует, то возвращает существующий id """
    with db.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO companies (employer_id, name)
            VALUES (%s, %s)
            ON CONFLICT (employer_id) DO NOTHING
            RETURNING id;
        """, (employer_id, name))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            # Получаем id компании, если уже существует
            cursor.execute("SELECT id FROM companies WHERE employer_id = %s", (employer_id,))
            return cursor.fetchone()[0]

def insert_vacancies(db: DBManager, company_id: int, vacancies: list) -> None:
    """ Вставка списка вакансий для заданной компании """
    with db.connection.cursor() as cursor:
        for vacancy in vacancies:
            cursor.execute("""
                            INSERT INTO vacancies (company_id, title, salary_from, salary_to, url)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
                        """, (
                company_id,
                vacancy['title'],
                vacancy['salary_from'],
                vacancy['salary_to'],
                vacancy['url']
            ))

def main():
    # Инициализация DBManager и создание таблиц в БД
    db = DBManager(DSN)
    db.create_tables()

    # Список выбранных работодателей (employer_id)
    employer_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for employer_id in employer_ids:
        employer_data = api.get_employer_data(employer_id)
        if not employer_data:
            print(f"Не удалось получить данные для employer_id {employer_id}")
            continue

        company_name = employer_data.get("name")
        company_id = insert_company(db, employer_id, company_name)

        # Получение вакансий, обработка их и сохранение в БД
        raw_vacancies = api.get_all_vacancies(employer_id)
        processed_vacancies = vacancy_manager.process_vacancies(raw_vacancies)
        insert_vacancies(db, company_id, processed_vacancies)
        print(f"Обработаны данные для компании: {company_name}")

    # Демонстрация работы методов DBManager
    companies_vacancies = db.get_companies_and_vacancies_count()
    print("\nКомпании и количество вакансий:")
    for company in companies_vacancies:
        print(f"{company['company']}: {company['vacancies_count']} вакансий")

    avg_salary = db.get_avg_salary()
    print(f"\тСредняя зарплата по вакансиям: {avg_salary}")

    keyword = input("\nВведите ключевое слово для поиска вакансий: ")
    vacancies_with_keyword = db.get_vacancies_with_keyword(keyword)
    print(f"\nВакансии, содержащие слово '{keyword}':")
    for vac in vacancies_with_keyword:
        print(f"{vac['company']} - {vac['title']} (з/п: {vac['salary_from']} - {vac['salary_to']}) {vac['url']}")

    db.close()

if __name__ == '__main__':
    main()

