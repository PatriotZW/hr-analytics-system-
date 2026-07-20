import pytest

from repositories.company_repository import CompanyRepository
from storage.json_storage import JsonStorage
from services.hr_service import HRService
from models.company import Company
from models.department import Department


def test_constructor_stores_repository(tmp_path):
    storage = JsonStorage(tmp_path / "company.json")
    repository = CompanyRepository(storage)

    service = HRService(repository)

    assert service.repository is repository


def test_constructor_rejects_invalid_repository():
    with pytest.raises(TypeError):
        HRService(12)

def test_transfer_employee_changes_department():
    company = Company("Peck Solutions")

    hr = Department("HR")
    it = Department("IT")

    company.add_department(hr)
    company.add_department(it)

    employee = company.hire_employee(
        name="John Smith",
        department_id=hr.department_id,
        salary=2500,
    )

    transferred_employee = company.transfer_employee(
        employee.employee_id,
        it.department_id,
    )

    assert transferred_employee is employee
    assert employee.department_id == it.department_id

def test_transfer_employee_rejects_same_department():
    company = Company("Peck Solutions")

    department = Department("IT")
    company.add_department(department)

    employee = company.hire_employee(
        name="John Smith",
        department_id=department.department_id,
        salary=2500,
    )

    with pytest.raises(
        ValueError,
        match="Employee already belongs to this department",
    ):
        company.transfer_employee(
            employee.employee_id,
            department.department_id,
        )


def test_transfer_employee_rejects_inactive_department():
    company = Company("Peck Solutions")

    hr = Department("HR")
    it = Department("IT")

    company.add_department(hr)
    company.add_department(it)

    employee = company.hire_employee(
        name="John Smith",
        department_id=hr.department_id,
        salary=2500,
    )

    company.deactivate_department(
        department_id=it.department_id,
    )

    with pytest.raises(
        ValueError,
        match="Cannot transfer an employee to an inactive department",
    ):
        company.transfer_employee(
            employee.employee_id,
            it.department_id,
        )


def test_save_and_load_transfer_round_trip(tmp_path):

    storage = JsonStorage(tmp_path / "company.json")
    repository = CompanyRepository(storage)
    service = HRService(repository)

    company = Company("Peck Solutions")
    hr = Department("HR")
    it = Department("IT")

    company.add_department(hr)
    company.add_department(it)

    repository.save(company)

    employee = service.hire_employee(
        name="John Smith",
        department_id=hr.department_id,
        salary=2500,
    )

    service.transfer_employee(
    employee.employee_id,
    it.department_id,
)
        
    loaded = repository.load()

    loaded_employee = loaded.find_employee_by_id(
    employee.employee_id,
)

    assert loaded_employee.department_id == it.department_id
    
def test_save_and_load_change_salary_round_trip(tmp_path):
    storage = JsonStorage(tmp_path / "company.json")
    repository = CompanyRepository(storage)
    service = HRService(repository)

    company = Company("Peck Solutions")
    hr = Department("HR")

    company.add_department(hr)
    repository.save(company)

    employee = service.hire_employee(
        name="John Smith",
        department_id=hr.department_id,
        salary=2500,
    )

    new_salary = 3000

    updated_employee = service.change_salary(
        employee.employee_id,
        new_salary,
    )

    loaded = repository.load()

    loaded_employee = loaded.find_employee_by_id(
        employee.employee_id,
    )

    assert updated_employee.salary == new_salary
    assert loaded_employee.salary == new_salary
