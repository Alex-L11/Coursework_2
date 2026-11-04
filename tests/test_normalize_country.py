from src.normalize_country import normalize_country, name_country_latin


def test_normalize_country_success():
    name = normalize_country('usa')
    assert name == 'United States'


def test_normalize_country_error():
    name = normalize_country('germania')
    assert name is None


def test_country_latin_success():
    country_1 = name_country_latin('caNada')
    country_2 = name_country_latin('caнada')

    assert country_1 == True
    assert country_2 == False
