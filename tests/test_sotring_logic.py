from src.sorting_logic import AircraftSorting


def test_top_altitude(data_aircraft_3: list) -> None:
    alt = AircraftSorting.top_altitude(data_aircraft_3, 2)
    alt_1 = AircraftSorting.top_altitude(data_aircraft_3, 0)
    alt_0 = AircraftSorting.top_altitude(data_aircraft_3, "")  # type: ignore[arg-type]

    assert len(alt) == 2
    assert alt_1 == []
    assert alt_0 == []


def test_filter_by_country(data_aircraft_3: list) -> None:
    country = AircraftSorting.filter_by_country(data_aircraft_3, ["Spain"])

    assert len(country) == 2


def test_filter_by_country_error(data_aircraft_3: list) -> None:
    country = AircraftSorting.filter_by_country(data_aircraft_3, [])

    assert country == []


def test_top_velocity_success(data_aircraft_3: list) -> None:
    vel = AircraftSorting.top_velocity(data_aircraft_3, 3)
    vel_1 = AircraftSorting.top_velocity(data_aircraft_3, [])  # type: ignore[arg-type]

    assert len(vel) == 3
    assert vel[0].velocity == 250.7
    assert vel[1].velocity == 200.7
    assert vel_1 == []


def test_filter_by_on_ground_success(data_aircraft_3: list) -> None:
    gr = AircraftSorting.filter_by_on_ground(data_aircraft_3, False)
    gr_1 = AircraftSorting.filter_by_on_ground(data_aircraft_3, True)

    assert len(gr) == 3
    assert len(gr_1) == 4
