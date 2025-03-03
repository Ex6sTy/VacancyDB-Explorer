import requests
from typing import Optional, Dict, Any, List

BASE_URL = "https://api.hh.ru"

def get_employer_data(employer_id: int) -> Optional[Dict[str, Any]]:
    """ Получает данные о работодателе и его идентификатору """
    url = f"{BASE_URL}/employers/{employer_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка запроса данных работодателя {employer_id}: {e}")
        return None

    def get_vacancies(employer_id: int, page: int = 0, per_page: int = 20) -> Optional[Dict[str, Any]]:
        """ Получает список вакансий работодателя с указанной страницы """
        url = f"{BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": per_page,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка запроса вакансий для работодателя {employer_id} на странице {page}: {e}")
            return None

        def get_all_vacancies(employer_id: int) -> List[Dict[str, Any]]:
            """ Получает все вакансии работодателя, обходя все страницы результатов """
            vacancies: List[Dict[str, Any]] = []
            page = 0

            while True:
                data = get_vacancies(employer_id, page)
                if data is None:
                    break
                items = data("items", [])
                vacancies.extend(items)
                total_pages = data.get("pages", 0)
                if page >= total_pages - 1:
                    break
                page += 1

            return vacancies

