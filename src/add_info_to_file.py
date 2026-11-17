import json
import os
from abc import ABC, abstractmethod
from os.path import abspath
from typing import Any, Optional

from src.data_for_planes import Aircraft


class AircraftStorage(ABC):
    """Абстрактный класс-коннектор для хранения данных о воздушных судах"""

    @abstractmethod
    def add_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет информацию о воздушном судне в файл"""
        pass

    @abstractmethod
    def get_aircraft(self, criteria: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Получает данные из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_aircraft(self, criteria: Optional[dict[str, Any]] = None) -> int:
        """Удаляет записи по критериям и возвращает количетсво удаленных записей"""
        pass


class SetupFile:
    """Создает файл, если его нет"""

    DEFAULT_DICT = {"version": "1.0", "records": []}

    @classmethod
    def setup_file(cls, file_name: str) -> str:
        dir_name = os.path.dirname(os.path.dirname((abspath(__file__))))
        dir_way = os.path.join(dir_name, "data", file_name)
        file_path = os.path.abspath(dir_way)

        # Если файла нет, создаем его
        if not os.path.isfile(dir_way):
            with open(dir_way, "w", encoding="utf-8") as f:
                json.dump(cls.DEFAULT_DICT, f, ensure_ascii=False, indent=4)

        return file_path


class JSONAircraftStorage(AircraftStorage):
    """Принимает название файла. Возвращает, добавляет или удаляет информацию о самолетах"""

    def __init__(self, file_name: str, file_path: Optional[str] = None) -> None:
        if file_path:
            self.file_path = file_path
        elif file_name:
            self.file_path = SetupFile.setup_file(file_name)
        else:
            raise ValueError("Нужно указать имя или путь файла")

    @staticmethod
    def read_data(file_path: str) -> dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "aircraft" not in data or not isinstance(data["aircraft"], list):
                return {"version": 1.0, "aircraft": []}
            return data  # type: ignore[no-any-return]

        except FileNotFoundError:
            return {"version": 1.0, "aircraft": []}

    @staticmethod
    def write_data(file_path: str, data: dict[str, Any]) -> None:
        payload = {"version": 1.0, "aircraft": data}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

    def get_aircraft(self, criteria: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Возвращает информацию о самолетах по указанным критериям"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "aircraft" not in data or not isinstance(data["aircraft"], list):
                return []

            raw_aircraft = data.get("aircraft", [])

            result: list[dict[str, Any]] = []
            for aircraft in raw_aircraft:
                if not criteria:
                    result.append(aircraft)
                    continue

                crit = True
                for key, value in criteria.items():
                    if key not in aircraft or aircraft[key] != value:
                        crit = False
                        break

                if crit:
                    result.append(aircraft)

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            return []

        return result

    def add_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет воздушное судно в JSON-файл"""
        data = JSONAircraftStorage.read_data(self.file_path)
        data["aircraft"].append(aircraft.to_dict())
        JSONAircraftStorage.write_data(self.file_path, data["aircraft"])

    def delete_aircraft(self, criteria: Optional[dict[str, Any]] = None) -> int:
        """Принимает параметр по которому удалить самолеты из всего списка самолетов"""
        data = JSONAircraftStorage.read_data(self.file_path)
        planes = data.get("aircraft", [])

        filter_air = []
        removed_count = 0

        if criteria is None:
            removed_count = len(planes)
            data["aircraft"] = []

        else:
            for aircraft in planes:
                crit = True

                for key, value in criteria.items():
                    if key not in aircraft or aircraft[key] != value:
                        crit = False
                        break

                if crit:
                    removed_count += 1
                else:
                    filter_air.append(aircraft)

            data["aircraft"] = filter_air
        JSONAircraftStorage.write_data(self.file_path, data["aircraft"])
        return removed_count
