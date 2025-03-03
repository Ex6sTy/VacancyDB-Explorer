from src import api

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("Error")

    def json(self):
        return self._json

def dummy_get_employer(url, *args, **kwargs):
    # Имитируем ответ для запроса данных работодателя
    if "employers" in url:
        return DummyResponse({"name": "Test Company", "id": 123}, 200)
    raise Exception("Invalid URL")

def dummy_get_vacancies(url, params, *args, **kwargs):
    # Имитируем пагинацию вакансий
    if "vacancies" in url:
        page = params.get("page", 0)
        if page == 0:
            # Первая страница содержит 1 вакансию, и общее число страниц = 2
            return DummyResponse({"items": [{
                "name": "Developer",
                "alternate_url": "http://example.com/vacancy/1",
                "salary": {"from": 1000, "to": 2000}
            }], "pages": 2})
        else:
            # Вторая страница с одной вакансией
            return DummyResponse({"items": [{
                "name": "Tester",
                "alternate_url": "http://example.com/vacancy/2",
                "salary": None
            }], "pages": 2})
    raise Exception("Invalid URL")

def test_get_employer_data(monkeypatch):
    """
    Тестирует функцию получения данных работодателя.
    """
    monkeypatch.setattr(api.requests, "get", lambda url, *args, **kwargs: dummy_get_employer(url, *args, **kwargs))
    data = api.get_employer_data(123)
    assert data is not None
    assert data["name"] == "Test Company"

def test_get_all_vacancies(monkeypatch):
    """
    Тестирует функцию получения всех вакансий с имитацией пагинации.
    """
    monkeypatch.setattr(api.requests, "get", lambda url, **kwargs: dummy_get_vacancies(url, kwargs.get("params", {})))
    vacancies = api.get_all_vacancies(123)
    # Ожидаем 2 вакансии (с двух страниц)
    assert isinstance(vacancies, list)
    assert len(vacancies) == 2
