from src.normalize_country import name_latin, normalize_country


def test_normalize_country_success() -> None:
    name = normalize_country("usa")
    assert name == "United States"


def test_normalize_country_error() -> None:
    name = normalize_country("germania")
    assert name is None


def test_name_latin_success() -> None:
    country_1 = name_latin("caNada")
    country_2 = name_latin("caнada")

    assert country_1
    assert not country_2
