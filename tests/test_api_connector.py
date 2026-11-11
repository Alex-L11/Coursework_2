from unittest.mock import Mock, patch

import pytest

from src.api_connector import GetCoordinate, InfoPlanes


@patch("requests.get")
def test_get_coordinate_success(mock_requests: Mock, coordinates: dict, nominatim: list[dict]) -> None:
    mock_response = Mock()
    mock_response.json.return_value = nominatim
    mock_requests.return_value = mock_response

    api = GetCoordinate("Canada")
    assert api.get_api_request() == coordinates


@patch("requests.get")
def test_get_coordinate_error(mock_requests: Mock, without_coordinate: dict) -> None:
    mock_response = Mock()
    mock_response.json.return_value = without_coordinate
    mock_requests.return_value = mock_response
    with pytest.raises(ValueError):
        api = GetCoordinate("canada")
        api.get_api_request()


@patch("requests.get")
def test_get_coordinate_error_1(mock_requests: Mock, error_nominatim: dict) -> None:
    mock_response = Mock()
    mock_response.json.return_value = error_nominatim
    mock_requests.return_value = mock_response
    api = GetCoordinate("canada")

    with pytest.raises(ValueError, match="Некорректный формат координат"):
        api.get_api_request()


@patch("requests.get")
def test_get_coordinate_data_error(mock_requests: Mock) -> None:
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_requests.return_value = mock_response
    api = GetCoordinate("canada")

    with pytest.raises(ValueError, match="Координаты не найдены для указанной страны"):
        api.get_api_request()


@patch("requests.get")
def test_info_planes_success(mock_requests: Mock, coordinates: dict, aircraft: dict) -> None:
    mock_response = Mock()
    mock_response.json.return_value = aircraft
    mock_requests.return_value = mock_response

    api = InfoPlanes(coordinates)
    assert api.get_api_request() == aircraft
