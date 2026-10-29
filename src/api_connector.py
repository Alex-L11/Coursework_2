from abc import ABC, abstractmethod
from requests import get
from typing import Any
from tenacity import retry, stop_after_attempt, wait_fixed

class APIService(ABC):

    @abstractmethod
    def get_coordinate(self, country: str) -> dict[str, Any]:
        pass


class GetCoordinate(APIService):
    """ Класс для получения координат из API сервиса Nominatim """
    def __init__(self) -> None:
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'

    def get_coordinate(self, country: str) -> dict[str, Any]:


        # Обязательный параметр User-Agent при запросе к nominatim.openstreetmap
        headers_nominatim = {
            'User-Agent': 'test-app'
        }
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Получение координат
        if not data:
            raise ValueError('Координаты не найдены для указанной страны')

        geo_coordinates = data[0].get('boundingbox')

        if geo_coordinates is None or len(geo_coordinates) != 4:
            raise ValueError('Некорректный формат координат')

        return {
                'lamin': geo_coordinates[0],
                'lamax': geo_coordinates[1],
                'lomin': geo_coordinates[2],
                'lomax': geo_coordinates[3],
            }


class InfoPlanes:

    def __init__(self):
        self.opensky_url = 'https://opensky-network.org/api/states/all'

    def get_info_planes(self, geo_coordinate: dict) -> dict[str, Any]:
                
        params = {
            'lamin': geo_coordinate['lamin'],
            'lamax': geo_coordinate['lamax'],
            'lomin': geo_coordinate['lomin'],
            'lomax': geo_coordinate['lomax'],
        }

        if len(params) != 4:
            raise KeyError('Не хватает координат')
        response = get(url=self.opensky_url, params=params, timeout=10)
        response.raise_for_status()

        info_planes = response.json()

        if 'states' not in info_planes:
            raise ValueError('Неожиданный формат ответа от OpenSky')

        return info_planes


if __name__ == '__main__':

    api = GetCoordinate()
    coordinates = api.get_coordinate('Canada')
    print("Границы:", coordinates)

    client = InfoPlanes()
    result = client.get_info_planes(coordinates)

    print("Время данных:", result.get('time'))
    print("Количество самолётов:", len(result['states']))