import json
from src.file_manager import save_data_to_json, load_data_from_json


def test_save_and_load(tmp_path):
    """
    Тестирует сохранение и последующую загрузку данных в JSON.
    """
    file_path = tmp_path / "test.json"
    data = {"key": "value", "number": 123}

    # Сохраняем данные в файл
    save_data_to_json(data, str(file_path))

    # Проверяем, что файл создан
    assert file_path.exists()

    # Загружаем данные и сравниваем с исходными
    loaded_data = load_data_from_json(str(file_path))
    assert loaded_data == data
