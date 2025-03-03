import json
from typing import Any

def save_data_to_json(data: Any, filename: str) -> None:
    """ Сохранение данных в JSON-файл """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно загружены в {filename}")
    except IOError as e:
        print(f"Ошибка сохранения данных в {filename}: {e}")

def load_data_from_json(filename: str) -> Any:
    """ Загружает данные из JSON-файла """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"Данные успешно загружены из {filename}")
        return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки данных из {filename}: {e}")
        return None
    