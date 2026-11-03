import pytest

from unittest.mock import Mock, patch

from src.api_connector import GetCoordinate, InfoPlanes

@patch('requests.get')
def test_get_coordinate_success(mock_requests, coordinates, nominatim):
    mock_response = Mock()
    mock_response.json.return_value = nominatim
    mock_requests.return_value = mock_response

    api = GetCoordinate()
    assert api.get_coordinate('Canada') == coordinates


@patch('requests.get')
def test_get_coordinate_error(mock_requests, without_coordinate):
    mock_response = Mock()
    mock_response.json.return_value = without_coordinate
    mock_requests.return_value = mock_response
    with pytest.raises(ValueError):
        api = GetCoordinate()
        api.get_coordinate('canada')


@patch('requests.get')
def test_get_coordinate_error_1(mock_requests, error_nominatim):
    mock_response = Mock()
    mock_response.json.return_value = error_nominatim
    mock_requests.return_value = mock_response
    api = GetCoordinate()

    with pytest.raises(ValueError, match='Некорректный формат координат'):
        api.get_coordinate('canada')


@patch('requests.get')
def test_get_coordinate_data_error(mock_requests):
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_requests.return_value = mock_response
    api = GetCoordinate()

    with pytest.raises(ValueError, match='Координаты не найдены для указанной страны'):
        api.get_coordinate('canada')


@patch('requests.get')
def test_info_planes_success(mock_requests, coordinates, aircraft):
    mock_response = Mock()
    mock_response.json.return_value = aircraft
    mock_requests.return_value = mock_response

    api = InfoPlanes()
    assert api.get_info_planes(coordinates) == aircraft