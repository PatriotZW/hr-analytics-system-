# ============================================================
# Third-Party Imports
# ============================================================

import pytest
import json

# ============================================================
# Local Application Imports
# ============================================================

from repositories.company_repository import CompanyRepository
from storage.json_storage import JsonStorage
from models.company import Company
from models.department import Department
from models.employee import Employee

def test_constructor_stores_storage(tmp_path):
    storage = JsonStorage(tmp_path / "company.json")

    repository = CompanyRepository(storage)

    assert repository.storage is storage

def test_constructor_rejects_invalid_storage():
    with pytest.raises(TypeError):
        CompanyRepository("data/company.json")

def test_save_writes_company_dictionary(tmp_path):
    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
    )
    company.add_employee(employee)

    expected = company.to_dict()

    storage = JsonStorage(tmp_path / "company.json")
    repository = CompanyRepository(storage)

    repository.save(company)

    with open(tmp_path / "company.json", "r", encoding="utf-8") as file:
        actual = json.load(file)

    assert actual == expected

def test_load_returns_reconstructed_company(tmp_path):
    data = {
        "company": {
            "name": "Peck Solutions",
        },
        "departments": [
            {
                "department_id": "DEP001",
                "name": "Human Resources",
                "status": "ACTIVE",
            }
        ],
        "employees": [
            {
                "employee_id": "EMP1000",
                "name": "John Smith",
                "department_id": "DEP001",
                "salary": 2500,
                "manager_id": None,
                "status": "ACTIVE",
            }
        ],
    }

    storage = JsonStorage(tmp_path / "company.json")
    storage.save(data)

    repository = CompanyRepository(storage)

    company = repository.load()

    assert company.to_dict() == data


def test_save_and_load_round_trip(tmp_path):

    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
    )
    company.add_employee(employee)

    storage = JsonStorage(tmp_path / "company.json")
    repository = CompanyRepository(storage)
    repository.save(company)

    loaded_company = repository.load()

    assert company.to_dict() == loaded_company.to_dict()
