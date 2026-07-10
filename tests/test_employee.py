from models.employee import Employee, EmployeeStatus


def test_create_employee():
    employee = Employee(" john smith ", " dep001 ", 2500)

    assert employee.name == "John Smith"
    assert employee.department_id == "DEP001"
    assert employee.salary == 2500
    assert employee.status == EmployeeStatus.ACTIVE
    assert employee.employee_id.startswith("EMP")


def test_invalid_name():
    try:
        Employee(" ", "DEP001", 2500)
        assert False
    except ValueError:
        assert True


def test_invalid_salary():
    try:
        Employee("John Smith", "DEP001", -500)
        assert False
    except ValueError:
        assert True


def test_deactivate_employee():
    employee = Employee("John Smith", "DEP001", 2500)

    employee.deactivate()

    assert employee.status == EmployeeStatus.INACTIVE


def test_to_dict():
    employee = Employee("John Smith", "DEP001", 2500)

    data = employee.to_dict()

    assert data["name"] == "John Smith"
    assert data["department_id"] == "DEP001"
    assert data["status"] == "ACTIVE"


def test_from_dict():
    data = {
        "employee_id": "EMP2000",
        "name": "John Smith",
        "department_id": "DEP001",
        "salary": 2500,
        "manager_id": None,
        "status": "ACTIVE",
    }

    employee = Employee.from_dict(data)

    assert employee.employee_id == "EMP2000"
    assert employee.name == "John Smith"
    assert employee.status == EmployeeStatus.ACTIVE

def test_department_id_is_normalized():
    employee = Employee("John Smith", " dep001 ", 2500)

    assert employee.department_id == "DEP001"

def test_manager_id_is_normalized():
    employee = Employee(
        "John Smith",
        "DEP001",
        2500,
        manager_id=" emp1000 "
    )

    assert employee.manager_id == "EMP1000"

import pytest

def test_employee_id_is_immutable():
    employee = Employee("John Smith", "DEP001", 2500)

    with pytest.raises(AttributeError):
        employee.employee_id = "EMP9999"