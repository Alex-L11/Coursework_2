import json
from typing import Any

import pytest

from src.data_for_planes import Aircraft


@pytest.fixture
def coordinates() -> dict:
    return {"lamin": "41.6765597", "lamax": "83.3362128", "lomin": "-141.00275", "lomax": "-52.3237664"}


@pytest.fixture
def nominatim() -> list[dict]:
    return [{"boundingbox": ["41.6765597", "83.3362128", "-141.00275", "-52.3237664"]}]


@pytest.fixture
def error_nominatim() -> list[dict]:
    return [{"boundingbox": ["41.6765597", "83.3362128", "-141.00275"]}]


@pytest.fixture
def without_coordinate() -> list[dict]:
    return [{"boundingbox": []}]


@pytest.fixture
def aircraft() -> dict[str, Any]:
    return json.loads("""{
        "time": 1766166618,
        "states": [
            ["4b1812", "SWR438A", "United States", 1766166618, 1766166618,
            -0.0168, 51.0888, 4267.2, false, 189.7, 129.39, 14.63,
            null, 4282.44, "2061", false, 0]
            ]
    }
    """)


@pytest.fixture
def aircraft_error_1() -> dict[str, Any]:
    return json.loads("""{
    "time": 1766166618,
        "states": [
            ["4b1812", "ABC438A", "Spain", 1766166618, 1766166618,
            -0.0168, 51.0888, 4267.2, false, -189.7, 129.39, 14.63,
            null, 4282.44, "2061", false, 0]
            ]
    }
    """)


@pytest.fixture
def aircraft_1() -> Aircraft:
    return Aircraft("4b1812", "Spain", 189.7, 4282.44, False)


@pytest.fixture
def aircraft_2() -> Aircraft:
    return Aircraft("4b1812", "Spain", 200.7, 3282.44, False)


@pytest.fixture
def aircraft_3() -> Aircraft:
    return Aircraft("4b1812", "Spain", 250.7, 3842.44, False)


@pytest.fixture
def aircraft_4() -> Aircraft:
    return Aircraft("dsa3532", "Italy", 189.7, 4282.44, False)


@pytest.fixture
def data_aircraft() -> dict:
    return {
        "version": 1.0,
        "aircraft": [
            {"bort_number": "avsd2341", "country": "Russia", "speed": 800},
            {"bort_number": "xyz999", "country": "USA", "speed": 900},
        ],
    }


@pytest.fixture
def data_aircraft_2() -> dict:
    return {
        "version": 1.0,
        "aircraft": [
            {"bort_number": "avsd2341", "country": "Russia", "speed": 800},
            {"bort_number": "abc666", "country": "Spain", "speed": 900},
            {"bort_number": "xyz999", "country": "USA", "speed": 1000},
        ],
    }


@pytest.fixture
def data_aircraft_3() -> list[Aircraft]:
    return [
        Aircraft("4b1812", "United States", 189.7, 4282.44, False),
        Aircraft("4b1812", "Spain", 200.7, 3282.44, False),
        Aircraft("4b1812", "Spain", 250.7, 3842.44, True),
        Aircraft("dsa3532", "Italy", 189.7, 4282.44, False),
    ]
