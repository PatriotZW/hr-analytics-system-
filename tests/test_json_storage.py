# ============================================================
# Standard Library Imports
# ============================================================

from pathlib import Path
import json
import pytest

# ============================================================
# Local Application Imports
# ============================================================

from storage.json_storage import JsonStorage

def test_constructor_stores_path():
    storage = JsonStorage("data/company.json")

    assert storage.file_path == Path("data/company.json")

def test_file_path_returns_path_object():
    storage = JsonStorage("data/company.json")

    assert isinstance(storage.file_path, Path)


def test_save_dictionary(tmp_path):
    file_path = tmp_path / "company.json"
    storage = JsonStorage(file_path)

    data = {
        "name": "Peck Solutions",
        "status": "ACTIVE",
    }

    storage.save(data)

    assert file_path.is_file()

def test_save_writes_dictionary_contents(tmp_path):
    file_path = tmp_path / "company.json"
    storage = JsonStorage(file_path)

    data = {
        "name": "Peck Solutions",
        "status": "ACTIVE",
    }

    storage.save(data)
    
    with file_path.open("r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)
    
    assert loaded_data == data

def test_save_rejects_none(tmp_path):
    file_path = tmp_path / "company.json"
    storage = JsonStorage(file_path)

    with pytest.raises(ValueError):
        storage.save(None)

def test_load_returns_dictionary(tmp_path):
    
    data = {
        "name": "Peck Solutions",
        "status": "ACTIVE",
    }

    file_path = tmp_path / "company.json"
    with file_path.open("w", encoding="utf-8",) as json_file:
        json.dump(data,json_file,indent=4,ensure_ascii=False,)

    storage = JsonStorage(file_path)
    loaded_data= storage.load()
    
    assert data == loaded_data

def test_load_returns_list(tmp_path):
    
    data = [1,2,3,4]
       
    file_path = tmp_path / "company.json"
    with file_path.open("w", encoding="utf-8",) as json_file:
        json.dump(data,json_file,indent=4,ensure_ascii=False,)

    storage = JsonStorage(file_path)
    loaded_data = storage.load()
    
    assert data == loaded_data

def test_load_raises_file_not_found(tmp_path):
    storage = JsonStorage(tmp_path)

    with pytest.raises(FileNotFoundError):
        storage.load()
