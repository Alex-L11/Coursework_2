from abc import ABC, abstractmethod
from typing import Any

import requests


class APIService(ABC):

    @abstractmethod
    def get_api_request(self) -> dict[str, Any]:
        pass


class GetCoordinate(APIService):
    """Класс для получения координат из API сервиса Nominatim"""

    def __init__(self, country: str) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.country = country

    def get_api_request(self) -> dict[str, Any]:

        # Обязательный параметр User-Agent при запросе к nominatim.openstreetmap
        headers_nominatim = {"User-Agent": "test-app"}
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim: dict[str, Any] = {
            "country": self.country,
            "format": "json",
            "limit": 1,
        }

        response = requests.get(
            url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim, timeout=10
        )
        response.raise_for_status()

        data = response.json()

        # Получение координат
        if not data:
            raise ValueError("Координаты не найдены для указанной страны")

        geo_coordinates = data[0].get("boundingbox")

        if geo_coordinates is None or len(geo_coordinates) != 4:
            raise ValueError("Некорректный формат координат")

        return {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }


class InfoPlanes(APIService):
    """Класс для получения информации о самолетах в заданных координатах"""

    def __init__(self, geo_coordinate: dict[str, float]) -> None:
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.geo_coordinate = geo_coordinate

    def get_api_request(self) -> dict[str, Any]:
        params = {
            "lamin": self.geo_coordinate["lamin"],
            "lamax": self.geo_coordinate["lamax"],
            "lomin": self.geo_coordinate["lomin"],
            "lomax": self.geo_coordinate["lomax"],
        }

        response = requests.get(url=self.opensky_url, params=params, timeout=10)
        response.raise_for_status()

        info_planes: dict = response.json()

        if "states" not in info_planes:
            raise ValueError("Неожиданный формат ответа от OpenSky")

        return info_planes
