import json
import os
from pathlib import Path

import pytest

import src.data_for_planes
from src.add_info_to_file import JSONAircraftStorage, ReadWriteJSON, SetupFile
from src.data_for_planes import Aircraft


def test_setup_file() -> None:
    file_way = SetupFile.setup_file("test_add_file.json")

    assert os.path.isabs(file_way)
    assert "data" in file_way
    assert os.path.basename(file_way) == "test_add_file.json"

    expected_dir = os.path.dirname(os.path.dirname(os.path.abspath(src.add_info_to_file.__file__)))
    expected_path = os.path.abspath(os.path.join(expected_dir, "data", "test_add_file.json"))

    assert expected_path == file_way


def test_read_file(tmp_path: Path) -> None:
    file = tmp_path / "good.json"
    file_1 = tmp_path / "bad.json"
    file.write_text(json.dumps({"version": 1.0, "aircraft": [{"bort_number": "avsd2341"}]}), encoding="utf-8")

    data = ReadWriteJSON.read_data(str(file))
    file_1.write_text(json.dumps({"version": 3.0, "aircraft": []}))

    data_1 = ReadWriteJSON.read_data((str(file_1)))

    assert data == {"version": 1.0, "aircraft": [{"bort_number": "avsd2341"}]}
    assert data_1 == {"version": 3.0, "aircraft": []}


def test_read_file_error(tmp_path: Path) -> None:
    file = tmp_path / "bad.json"
    file.write_text(json.dumps({"version": 3.0, "aircraft": ""}))
    data = ReadWriteJSON.read_data(str(file))

    assert data == {"version": 1.0, "aircraft": []}


def test_read_file_error_1(tmp_path: Path) -> None:
    file = tmp_path / "no file.json"

    data = ReadWriteJSON.read_data(str(file))

    assert data == {"version": 1.0, "aircraft": []}


def test_get_aircraft_success(tmp_path: Path, data_aircraft: dict) -> None:
    file_path = tmp_path / "good.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_aircraft, f, ensure_ascii=False, indent=4)

    storage = JSONAircraftStorage("ignore_name", file_path=str(file_path))
    assert len(storage.get_aircraft()) == 2

    russian = storage.get_aircraft(criteria={"country": "Russia"})
    assert len(russian) == 1
    assert russian[0]["bort_number"] == "avsd2341"
    assert storage.get_aircraft(criteria={"country": "Canada"}) == []


def test_jsonircraftstorage_error() -> None:
    with pytest.raises(ValueError, match="Нужно указать имя или путь файла"):
        JSONAircraftStorage("")


def test_add_aircraft(tmp_path: Path, aircraft_1: Aircraft, data_aircraft: dict) -> None:
    file_path = tmp_path / "good.json"

    file_path.write_text(json.dumps(data_aircraft, ensure_ascii=False, indent=4), encoding="utf-8")

    storage = JSONAircraftStorage("ignore_name", file_path=str(file_path))
    storage.add_aircraft(aircraft_1)

    data = ReadWriteJSON.read_data(str(file_path))

    assert len(data["aircraft"]) == 3
    assert data["aircraft"][0]["bort_number"] == "avsd2341"
    assert data["aircraft"][2] == aircraft_1.to_dict()


def test_delete_aircraft(tmp_path: Path, data_aircraft_2: dict) -> None:
    file_path = tmp_path / "good.json"
    file_path.write_text(json.dumps(data_aircraft_2, ensure_ascii=False, indent=4), encoding="utf-8")
    storage = JSONAircraftStorage("file_name", file_path=str(file_path))

    count = storage.delete_aircraft(criteria={"country": "Spain"})
    data = ReadWriteJSON.read_data(str(file_path))

    assert count == 1
    assert len(data["aircraft"]) == 2
