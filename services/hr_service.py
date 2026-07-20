# ============================================================
# Local Application Imports
# ============================================================

from repositories.company_repository import CompanyRepository
from models.company import Company
from models.employee import Employee


class HRService:

    def __init__(self, repository: CompanyRepository):

        if not isinstance(repository, CompanyRepository):
            raise TypeError(
                "repository must be a CompanyRepository object."
            )

        self._repository = repository

        

    @property
    def repository(self) -> CompanyRepository:
        return self._repository
    
    def hire_employee(
    self,
    name: str,
    department_id: str,
    salary: float,
    manager_id: str | None = None,
) -> Employee:
        
        company = self.repository.load()

        employee = company.hire_employee(name, department_id, salary, manager_id,)

        self.repository.save(company)

        return employee
    
    def transfer_employee(
    self,
    employee_id: str,
    department_id: str,
) -> Employee:

        company = self.repository.load()

        employee = company.transfer_employee(
            employee_id,
            department_id,
        )

        self.repository.save(company)

        return employee
        
    def change_salary(
    self,
    employee_id: str,
    new_salary: float,
) ->Employee:
        company = self.repository.load()

        employee = company.change_salary(
            employee_id,
            new_salary,
        )

        self.repository.save(company)

        return employee