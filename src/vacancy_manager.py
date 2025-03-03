from typing import Dict, Any, List


def parse_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
    """ Преобразование данных вакансий из API в формат, пригодный для записи в базу данных """
    title = vacancy.get("name")
    url = vacancy.get("alternate_url")
    salary_info = vacancy.get("salary")
    salary_from = salary_to = None
    if salary_info:
        salary_from = salary_info.get("from")
        salary_to = salary_info.get("to")
    return {
        "title": title,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "url": url
    }

def process_vacancies(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Обрабатывает список вакансий, преобразуя каждую к требуемому формату """
    return [parse_vacancy(vacancy) for vacancy in vacancies]

def filter_vacancies_by_keyword(vacancies: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """ Фильтрация вакансий по заданному слову """
    keyword_lower = keyword.lower()
    return [
        vacancy for vacancy in vacancies
        if vacancy.get("title") and keyword_lower in vacancy.get("title").lower()
    ]
