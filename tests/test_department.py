# ============================================================
# Third-Party Imports
# ============================================================

import pytest

# ============================================================
# Local Application Imports
# ============================================================

from models.department import Department, DepartmentStatus


def test_create_department():
    department = Department(" human Resources ")

    assert department.name == "Human Resources"
    assert department.status == DepartmentStatus.ACTIVE
    assert department.department_id.startswith("DEP")


def test_invalid_department_name_raises_error():
    with pytest.raises(ValueError):
        Department(" ")


def test_deactivate_department():
    department = Department("Human Resources")

    department.deactivate()

    assert department.status == DepartmentStatus.INACTIVE


def test_department_name_is_normalized():
    department = Department("  human resources  ")

    assert department.name == "Human Resources"


def test_to_dict():
    department = Department("Human Resources")

    data = department.to_dict()

    assert data["name"] == "Human Resources"
    assert data["status"] == "ACTIVE"


def test_from_dict():
    data = {
        "department_id": "DEP100",
        "name": "Human Resources",
        "status": "ACTIVE",
    }

    department = Department.from_dict(data)

    assert department.department_id == "DEP100"
    assert department.name == "Human Resources"
    assert department.status == DepartmentStatus.ACTIVE


def test_department_id_is_immutable():
    department = Department("Human Resources")

    with pytest.raises(AttributeError):
        department.department_id = "DEP456"