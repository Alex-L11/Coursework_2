from typing import Any, Optional


class Aircraft:
    """Представляет данные об одном воздушном судне"""

    def __init__(
        self, bort_number: str, country_plane: str, velocity: float, geo_altitude: Optional[float], on_ground: bool
    ) -> None:
        if not isinstance(bort_number, str) or not bort_number.strip():
            raise ValueError("Номер борта должен быть не пустой")
        self.bort_number = bort_number
        if not isinstance(country_plane, str) or not country_plane.strip():
            raise ValueError("Не указана страна")
        self.country_plane = country_plane
        self.on_ground = on_ground
        if not isinstance(velocity, (int, float)):
            raise TypeError("Горизнтальная скорость должна быть числом")
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной или отсутсвовать")
        self.velocity = velocity
        if geo_altitude is None:
            self.geo_altitude = None
        else:
            if not isinstance(geo_altitude, (int, float)):
                raise TypeError("Высота должна быть числом")
            if geo_altitude < 0:
                raise ValueError("Высота не может быть отрицательной или отсутсвовать")
            self.geo_altitude = float(geo_altitude)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) == (other.velocity, other.geo_altitude)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) < (other.velocity, other.geo_altitude)

    def __str__(self) -> str:
        return (
            f"Борт {self.bort_number} | {self.country_plane} | "
            f"Высота {self.geo_altitude} м | скорость {self.velocity} м/с"
        )

    def to_dict(self) -> dict:
        """Преобразует объекты Aircraft в словарь"""
        return {
            "bort_number": self.bort_number,
            "country_plane": self.country_plane,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude,
            "on_ground": self.on_ground,
        }


class PlaneExtractor:
    """Принимает данные из API OpenSky и возвращает список объектов Aircraft"""

    @staticmethod
    def get_aeroplanes(raw_data: dict) -> list[Aircraft]:
        if not isinstance(raw_data, dict):
            raise TypeError("Входные данные ожидаются в виде словаря")

        states = raw_data.get("states")
        if states is None:
            raise ValueError("API не вернул список самолетов")

        if not isinstance(states, list):
            raise ValueError('В словаре должен быть ключ "states" со списком данных')

        plane_data = []
        for plane in states:
            if len(plane) < 17:
                continue
            bort = plane[0]
            country = plane[2]
            on_ground = plane[8]
            velocity = plane[9]
            geo_altitude = plane[13]

            try:
                plane_obj = Aircraft(bort, country, velocity, geo_altitude, on_ground)
                plane_data.append(plane_obj)
            except TypeError as t:
                print(f"Ошибка: {t}")
            except ValueError as v:
                print(f"Ошибка: {v} ")
        return plane_data
