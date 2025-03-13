from src.database import create_database, create_tables
from src.data_filler import fill_employers_table
from src.db_manager import DBManager

def main():
    database_name = 'hh_vacancies'
    employer_ids = ['15478', '23427', '3529', '1740', '78638', '2748', '3776', '4181', '3127', '2180']

    # Создание и заполнение базы данных
    create_database(database_name)
    create_tables(database_name)
    fill_employers_table(database_name, employer_ids)

    # Работа с базой данных через DBManager
    db_manager = DBManager(database_name)

    # Вывод списка компаний и количества вакансий
    print("Список компаний и количество вакансий:")
    for company, count in db_manager.get_companies_and_vacancies_count():
        print(f"{company}: {count} вакансий")

    # Вывод списка всех вакансий
    print("\nСписок всех вакансий:")
    for company, title, salary_from, salary_to, url in db_manager.get_all_vacancies():
        print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary_from}-{salary_to}, Ссылка: {url}")

    # Вывод средней зарплаты
    avg_salary = db_manager.get_avg_salary()
    if avg_salary is not None:
        print(f"\nСредняя зарплата по всем вакансиям: {avg_salary:.2f}")
    else:
        print("\nНевозможно рассчитать среднюю зарплату: данные отсутствуют.")

    # Поиск вакансий с зарплатой выше средней
    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(f"Вакансия: {vacancy[2]}, Зарплата: {vacancy[3]}-{vacancy[4]}")

    # Поиск вакансий по ключевому слову
    keyword = input("\nВведите ключевое слово для поиска вакансий (например, 'python'): ")
    print(f"\nВакансии с ключевым словом '{keyword}':")
    for vacancy in db_manager.get_vacancies_with_keyword(keyword):
        print(f"Вакансия: {vacancy[2]}, Ссылка: {vacancy[5]}")

    # Поиск вакансий по желаемой зарплате и ключевому слову
    try:
        desired_salary = int(input("\nВведите желаемую зарплату: "))
        desired_keyword = input("Введите ключевое слово для поиска вакансий: ")
        print(f"\nВакансии с зарплатой от {desired_salary} и ключевым словом '{desired_keyword}':")
        vacancies = db_manager.get_vacancies_by_salary_and_keyword(desired_salary, desired_keyword)
        if vacancies:
            for company, title, salary_from, salary_to, url in vacancies:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary_from}-{salary_to}, Ссылка: {url}")
        else:
            print("Нет подходящих вакансий.")
    except ValueError:
        print("Ошибка: введите корректное число для зарплаты.")

    db_manager.close()

if __name__ == "__main__":
    main()