from api_connector import GetCoordinate, InfoPlanes
from data_for_planes import PlaneExtractor
from src.normalize_country import normalize_country, name_country_latin
from src.sorting_logic import top_altitude, filter_by_country, top_velocity, filter_by_on_ground


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""
    print("Приветсвуем! Добро пожаловать в трекер самолётов.\n")

    while True:
        user_country = input("Введите название страны латиницей, для получения информации о самолётах: \n").strip()

        if not user_country:
            print("Введите еще раз, поле оказалось пустым.\n")
            continue

        if name_country_latin(user_country):
            country = normalize_country(user_country)

            if country is None:
                print(f"Страна '{user_country}' не распознана. Повторите ввод.\n")
                continue

            break
        else:
            print("Используйте только латинские буквы и пробелы.\n")

    while True:
        try:
            top_altitude_n = int(input("Сколько самолётов показать в топе по высоте?\n"
                          "Например, введите 5, чтобы увидеть 5 самых высоко летящих самолёта: \n"))

            if top_altitude_n <= 0:
                print("Число должно быть больше 0. Попробуйте еще раз\n")
                continue
            break
        except ValueError:
            print("Введите корректное число")

    while True:
        try:
            top_velocity_n = int(input("Сколько самолётов показать в топе по скорости?\n"
                          "Например, введите 5, чтобы увидеть 5 самых быстрых самолёта: \n"))

            if top_velocity_n <= 0:
                print("Число должно быть больше 0. Попробуйте еще раз\n")
                continue
            break
        except ValueError:
            print("Введите корректное число")

    while True:
        raw_country = input("Для получения списка самолётов по стране регистрации, введите одну или несколько стран"
                        "(через запятую): \n")
        if not raw_country:
            print("Поле оказалось пустым, введите страну или страны")
            continue

        parts = [p.strip() for p in raw_country.split(",") if p.strip()]

        filter_countries = []
        for p in parts:
            if not name_country_latin(p):
                print(f"'{p}': используйте только латинские буквы.")
                continue
            normalized = normalize_country(p)
            if normalized:
                filter_countries.append(normalized)
            else:
                print(f"Не распознано: '{p}'")
        if filter_countries:
            break
        else:
            print(f"Ни одна из '{raw_country}' стран не распознана. Попробуйте еще раз.\n")

    while True:
        answer_ground = input("Оставить самолёты только те, которые в воздухе? Да/Нет \n").strip().lower()
        if answer_ground not in {'да', 'нет'}:
            print("Введите 'да' или 'нет'.")
            continue

        if answer_ground == 'да':
            include_on_ground = False
        else:
            include_on_ground = True
        break

    # Создание экземпляра класса для работы с API-сервисом
    api = GetCoordinate()

    # Получение координат по стране
    coordinates = api.get_coordinate(country)

    api_1 = InfoPlanes()
    raw_data = api_1.get_info_planes(coordinates)

    # Преобразование набора данных в список объектов
    aircraft_objects = PlaneExtractor.call_get_aeroplanes(raw_data)

    # Вывод топ самых высоких самолетов
    top_alt = top_altitude(aircraft_objects, top_altitude_n)

    # Вывод том самых быстрых самолета
    top_vel = top_velocity(aircraft_objects, top_velocity_n)

    # Вывод по странам регистрации самолетов
    filt_country = filter_by_country(aircraft_objects, filter_countries)

    # Вывод по странам регистрации самолетов которые на земле или в воздухе
    filter_by_ground = filter_by_on_ground(filt_country, include_on_ground=include_on_ground)

    print(f"\n---Всего самолетов {len(raw_data['states'])} ---")
    print()
    print(f"\n--- Топ самолётов по высоте: {top_altitude_n} ---")
    for plane in top_alt:
        print(plane)
    print()
    print(f"\n--- Топ {top_velocity_n} самых быстрых самолётов ---")
    for plane in top_vel:
        print(plane)
    print()
    print(f"\n--- Самолеты по странам регистрации {filter_countries} ---")
    print(f"Количество самолётов после фильтрации (в воздухе/на земле): {len(filter_by_ground)}")
    if not filter_by_ground:
        print("Самолётов, подходящих под оба условия, не найдено.\n")
    else:
        for plane in filter_by_ground:
            print(plane)

    # Запись данных в файл



if __name__ == '__main__':
    user_interaction()











