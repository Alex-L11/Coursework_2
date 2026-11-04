from src.data_for_planes import Aircraft


class AircraftSorting:
    @staticmethod
    def top_altitude(aircraft_list: list[Aircraft], n: int) -> list[Aircraft]:
        """Выводи топ-N по высоте"""
        if not n:
            return []
        elif n <= 0:
            return []

        sorted_aircraft = sorted(
            aircraft_list, key=lambda a: a.geo_altitude if a.geo_altitude is not None else float('-inf'), reverse=True
        )

        return sorted_aircraft[:n]

    @staticmethod
    def filter_by_country(aircraft_list: list[Aircraft], countries: list[str]) -> list[Aircraft]:
        """Выводит самолеты по стране"""
        if not countries:
            return []

        countries_set = set(countries)

        filter_list = []

        for plane in aircraft_list:
            if plane.country_plane in countries_set:
                filter_list.append(plane)
        return filter_list

    @staticmethod
    def top_velocity(aircraft_list: list[Aircraft], n: int) -> list[Aircraft]:
        """Выводит топ-N по скорости"""
        if not n:
            return []
        if n <= 0:
            return []

        sorted_aircraft = sorted(aircraft_list, key=lambda a: a.velocity, reverse=True)

        return sorted_aircraft[:n]

    @staticmethod
    def filter_by_on_ground(aircraft_list: list[Aircraft], include_on_ground: bool = False) -> list[Aircraft]:
        """Выводит список самолетов, которые в воздухе"""
        if include_on_ground:
            return aircraft_list

        return [a for a in aircraft_list if not a.on_ground]
