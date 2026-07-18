import pytest

from models.company import Company
from models.department import Department
from models.employee import Employee


def test_add_department_successfully():
    company = Company("Peck Solutions")
    department = Department("Human Resources")

    company.add_department(department)

    #assert department in company._departments
    assert department in company.departments

def test_add_department_rejects_wrong_type():
    company = Company("Peck Solutions")

    with pytest.raises(TypeError):
        company.add_department("Human Resources")


def test_add_department_rejects_duplicate_id():
    company = Company("Peck Solutions")
    first_department = Department("Human Resources")
    duplicate_department = Department("Finance")

    duplicate_department._department_id = first_department.department_id

    company.add_department(first_department)

    with pytest.raises(ValueError):
        company.add_department(duplicate_department)


def test_add_department_rejects_duplicate_name():
    company = Company("Peck Solutions")
    first_department = Department("Human Resources")
    duplicate_department = Department("human resources")

    company.add_department(first_department)

    with pytest.raises(ValueError):
        company.add_department(duplicate_department)


def test_add_inactive_department_successfully():
    company = Company("Peck Solutions")
    department = Department("Research And Development")
    department.deactivate()

    company.add_department(department)

    #assert department in company._departments
    assert department in company.departments


def test_add_employee_successfully():
    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500
    )

    company.add_employee(employee)

    assert employee in company.employees


def test_add_employee_rejects_wrong_type():
    company = Company("Peck Solutions")

    with pytest.raises(TypeError):
        company.add_employee("John Smith")


def test_add_employee_rejects_self_management():
    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
    )

    employee.manager_id = employee.employee_id

    with pytest.raises(ValueError):
        company.add_employee(employee)


def test_add_employee_rejects_unknown_manager():
    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
        manager_id="EMP9999",
    )

    with pytest.raises(ValueError):
        company.add_employee(employee)


def test_add_employee_rejects_duplicate_id():
    company = Company("Peck Solutions")
    department = Department("Human Resources")
    company.add_department(department)

    first_employee = Employee(
        "John Smith",
        department.department_id,
        2500
    )

    duplicate_employee = Employee(
        "John Smith",
        department.department_id,
        2500
    )
    

    duplicate_employee._employee_id = first_employee.employee_id

    company.add_employee(first_employee)

    with pytest.raises(ValueError):
        company.add_employee(duplicate_employee)


def test_add_employee_rejects_unknown_department():
    company = Company("Peck Solutions")

    employee = Employee(
        "John Smith",
        "DEP999",
        2500,
    )

    with pytest.raises(ValueError):
        company.add_employee(employee)


def test_find_employee_by_id():
    company = Company("Peck Solutions")

    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
    )

    company.add_employee(employee)

    result = company.find_employee_by_id(employee.employee_id)

    assert result is employee

    with pytest.raises(TypeError):
        company.find_employee_by_id(1000)


def test_find_department_by_id_returns_department():
    company = Company("Peck Solutions")
    department = Department("Human Resources")
    company.add_department(department)

    result = company.find_department_by_id(department.department_id)

    assert result is department


def test_find_employee_by_id_returns_employee():
    company = Company("Peck Solutions")
    department = Department("Human Resources")
    company.add_department(department)

    employee = Employee(
        "John Smith",
        department.department_id,
        2500,
    )
    company.add_employee(employee)

    result = company.find_employee_by_id(employee.employee_id)

    assert result is employee


def test_create_employee_successfully():
    employee = Employee("John Smith", "DEP001", 2500)

    #print(employee)

    assert employee.name == "John Smith"

def test_find_department_by_id_returns_none():
    company = Company("Peck Solutions")
    department = Department("Human Resources")
    company.add_department(department)
    result = company.find_department_by_id("DEP999")
    
    assert result is  None


def test_find_department_by_id_reject_non_string():
    company = Company("Peck Solutions")
    
    with pytest.raises(TypeError):
       company.find_department_by_id(2)


def test_find_employee_by_id_reject_non_string():
    company = Company("Peck Solutions")
    
    with pytest.raises(TypeError):
       company.find_employee_by_id(2)


def test_find_employee_by_id_returns_none():
    company = Company("Peck Solutions")
    department = Department("Human Resources")
    company.add_department(department)
    employee = Employee("John Smith",department.department_id,2500,)
    company.add_employee(employee)

    result = company.find_employee_by_id("EMP9999")
    
    assert result is  None


def test_departments_collection_is_read_only():
    company = Company("Peck Solutions")

    with pytest.raises(AttributeError):
        company.departments.append(Department("Finance"))


def test_employees_collection_is_read_only():
    company = Company("Peck Solutions")

    with pytest.raises(AttributeError):
        company.employees.append("employee")


def test_company_string_representation():
    company = Company("Peck Solutions")

    result = str(company)

    assert "Peck Solutions" in result
    assert "Departments : 0" in result
    assert "Employees   : 0" in result

def test_from_dict_reconstructs_company():
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

    company = Company.from_dict(data)

    assert company.name == "Peck Solutions"
    assert len(company.departments) == 1
    assert len(company.employees) == 1

    department = company.find_department_by_id("DEP001")
    employee = company.find_employee_by_id("EMP1000")

    assert department is not None
    assert department.name == "Human Resources"

    assert employee is not None
    assert employee.name == "John Smith"
    assert employee.department_id == "DEP001"

def test_from_dict_restores_employees_out_of_order():
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
                "manager_id": "EMP1002",
                "status": "ACTIVE",
            },

            {
                "employee_id": "EMP1001",
                "name": "Peter Andre",
                "department_id": "DEP001",
                "salary": 2500,
                "manager_id": "EMP1000",
                "status": "ACTIVE",
            },

            {
                "employee_id": "EMP1002",
                "name": "Mary Jones",
                "department_id": "DEP001",
                "salary": 2500,
                "manager_id": None,
                "status": "ACTIVE",
            }
        ],
    }


    company = Company.from_dict(data)

    assert company.name == "Peck Solutions"
    assert len(company.departments) == 1
    assert len(company.employees) == 3

    department = company.find_department_by_id("DEP001")
    john = company.find_employee_by_id("EMP1000")
    peter = company.find_employee_by_id("EMP1001")
    mary = company.find_employee_by_id("EMP1002")

    assert department is not None
    assert department.name == "Human Resources"

    assert john is not None
    assert peter is not None
    assert mary is not None
    
    assert john.manager_id == "EMP1002"
    assert peter.manager_id == "EMP1000"
    assert mary.manager_id is None

def test_from_dict_raises_value_error_for_circular_manager_relationships():
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
                "manager_id": "EMP1001",
                "status": "ACTIVE",
            },

            {
                "employee_id": "EMP1001",
                "name": "Peter Andre",
                "department_id": "DEP001",
                "salary": 2500,
                "manager_id": "EMP1000",
                "status": "ACTIVE",
            }

            ]
    }
          
    with pytest.raises(ValueError):
        Company.from_dict(data)

def test_from_dict_raises_value_error_for_missing_manager():
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
                "manager_id": "EMP9999",
                "status": "ACTIVE",
            }
            ]
    }
          
    with pytest.raises(ValueError):
        Company.from_dict(data)
