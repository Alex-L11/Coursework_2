import pytest

from src.data_for_planes import PlaneExtractor, Aircraft


def test_call_get_aeroplanes_error():
    with pytest.raises(TypeError, match="Входные данные ожидаются в виде словаря"):
        PlaneExtractor.call_get_aeroplanes(["no data"])

    with pytest.raises(ValueError, match="API не вернул список самолетов"):
        PlaneExtractor.call_get_aeroplanes({})

    with pytest.raises(ValueError, match='В словаре должен быть ключ "states" со списком данных'):
        PlaneExtractor.call_get_aeroplanes({'states': {}})


def test_call_get_aeroplanes_success(aircraft):
    obj = PlaneExtractor.call_get_aeroplanes(aircraft)
    assert len(obj) == 1
    assert obj[0].bort_number == "4b1812"
    assert obj[0].country_plane == "United States"
    assert obj[0].velocity == 189.7
    assert obj[0].on_ground is False
    assert obj[0].geo_altitude == 4282.44


def test_call_get_aeroplanes_error_obj(aircraft_error_1):
    obj = PlaneExtractor.call_get_aeroplanes(aircraft_error_1)
    assert len(obj) == 0


def test_aircraft_error_obj():

    with pytest.raises(TypeError, match="Горизнтальная скорость должна быть числом"):
        Aircraft("4b1812", "Spain", "189.7", 4282.44, False)

    with pytest.raises(ValueError, match="Номер борта должен быть не пустой"):
        Aircraft("", "Spain", 189.7, 4282.44, False)

    with pytest.raises(ValueError, match="Не указана страна"):
        Aircraft("ads4356", "", 189.7, 4282.44, False)

    with pytest.raises(ValueError, match="Скорость не может быть отрицательной или отсутсвовать"):
        Aircraft("4b1812", "Spain", -189.7, 4282.44, False)

    with pytest.raises(TypeError, match="Высота должна быть числом"):
        Aircraft("4b1812", "Spain", 189.7, "4282.44", False)

    with pytest.raises(ValueError, match="Высота не может быть отрицательной или отсутсвовать"):
        Aircraft("4b1812", "Spain", 189.7, -4282.44, False)


def test_aircraft_eq(aircraft_1, aircraft_2, aircraft_3, aircraft_4):
    assert aircraft_1 == aircraft_4
    assert aircraft_3 != aircraft_2


def test_aircraft_lt(aircraft_1, aircraft_2, aircraft_3, aircraft_4):
    assert aircraft_1 < aircraft_2
    assert aircraft_3 > aircraft_4

def test_aircraft_error_eq_lt(aircraft_1):
    other = 'no aircraft'

    assert aircraft_1 != other
    assert other != aircraft_1

    result = aircraft_1.__lt__(other)
    assert result is NotImplemented

    result_eq = aircraft_1.__eq__(other)
    assert result_eq is NotImplemented