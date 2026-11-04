import re
from typing import Optional

import pycountry

LATIN_PATTERN = re.compile(r'^[a-zA-Z\s]+$')


def normalize_country(name_country: str) -> Optional[str]:
    """Принимает страну или список стран, возвращает названия стран/ы согласно международным стандартам"""
    # Ищем страну по названию
    try:
        country = pycountry.countries.search_fuzzy(name_country)
    except LookupError:
        return None
    return country[0].name


def name_country_latin(country: str) -> bool:
    """Проверяет, чтобы в названии были только латинские буквы"""

    country = country.strip()

    if not country:
        return False

    return bool(LATIN_PATTERN.match(country))
