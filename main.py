from add_info_to_file import JSONAircraftStorage, SetupFile
from src.api_connector import GetCoordinate, InfoPlanes
from src.data_for_planes import PlaneExtractor
from src.normalize_country import normalize_country, name_latin
from src.sorting_logic import Aircraft, AircraftSorting


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""
    print("Приветсвуем! Добро пожаловать в трекер самолётов.\n")

    while True:
        user_country = input("Введите название страны латиницей, для получения информации о самолётах: \n").strip()

        if not user_country:
            print("Введите еще раз, поле оказалось пустым.\n")
            continue

        if name_latin(user_country):
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
            if not name_latin(p):
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

    while True:
        answer_by_file = input("Хотите записать данные в json-файл введите? Да/Нет \n").strip().lower()
        if answer_by_file not in {'да', 'нет'}:
            print("Введите 'да' или 'нет'.")
            continue
        if answer_by_file == 'да':
            save_to_file = input("Введите латинскими буквами имя файла без пробелов: \n")
            if name_latin(save_to_file):
                file_name = f'{save_to_file}.json'
                file_path = SetupFile.setup_file(file_name)
                break
            if save_to_file is None:
                print("Повторите ввод еще раз")
                continue
            break
        else:
            print("Используйте только латинские буквы.\n")

    # Создание экземпляра класса для работы с API-сервисом
    api = GetCoordinate(country)

    # Получение координат по стране
    coordinates = api.get_api_request()

    api_1 = InfoPlanes(coordinates)
    raw_data = api_1.get_api_request()

    # Преобразование набора данных в список объектов
    aircraft_objects = PlaneExtractor.get_aeroplanes(raw_data)

    # Вывод топ самых высоких самолетов
    top_alt = AircraftSorting.top_altitude(aircraft_objects, top_altitude_n)

    # Вывод том самых быстрых самолета
    top_vel = AircraftSorting.top_velocity(aircraft_objects, top_velocity_n)

    # Вывод по странам регистрации самолетов
    filt_country = AircraftSorting.filter_by_country(aircraft_objects, filter_countries)

    # Вывод по странам регистрации самолетов которые на земле или в воздухе
    filter_by_ground = AircraftSorting.filter_by_on_ground(filt_country, include_on_ground=include_on_ground)



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
    if save_to_file:
        data_dict = [plane.to_dict() for plane in filter_by_ground]
        JSONAircraftStorage.write_data(file_path, data_dict)
        print(f"Файл сохранен под именем '{save_to_file}'.\n")



if __name__ == '__main__':
    user_interaction()











