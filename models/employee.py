"""
Employee Module

Purpose
-------
Represents employees within the HR Analytics System.

Responsibilities
----------------
- Define the Employee model.
- Validate employee data.
- Manage employee state.
- Support serialization.

Does Not
--------
- Persist data.
- Generate reports.
- Perform analytics.
- Coordinate business operations.
"""

from enum import Enum
from typing import Optional


class EmployeeStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Employee:
    """
    Represents a single employee within the organisation.

    The Employee class is responsible for maintaining a valid
    employee throughout its lifetime.

    Every Employee has:

    - immutable employee_id
    - validated attributes
    - department reference
    - manager reference
    - employment status

    Business Rules:

    - Employee IDs are immutable.
    - Salary must be greater than zero.
    - Name cannot be blank.
    - Department is referenced by department_id.
    """    
    
    next_employee_id = 1000

    def __init__(
        self,
        name: str,
        department_id: str,
        salary: float,
        manager_id: Optional[str] = None,
        status: EmployeeStatus = EmployeeStatus.ACTIVE,
    ):
        self._employee_id = self._generate_employee_id()
        self.name = self._validate_name(name)
        self.department_id = self._validate_department_id(department_id)
        self.salary = self._validate_salary(salary)
        self.manager_id = manager_id
        self.status = self._validate_status(status)

    @classmethod
    def _generate_employee_id(cls) -> str:
        employee_id = f"EMP{cls.next_employee_id}"
        cls.next_employee_id += 1
        return employee_id

    @property
    def employee_id(self) -> str:
        return self._employee_id

    def _validate_name(self, name: str) -> str:
        name = name.strip().title()

        if not name:
            raise ValueError("Employee name cannot be blank.")

        return name

    def _validate_department_id(self, department_id: str) -> str:
        department_id = department_id.strip().upper()

        if not department_id:
            raise ValueError("Department ID cannot be blank.")

        return department_id

    def _validate_salary(self, salary: float) -> float:
        if salary <= 0:
            raise ValueError("Salary must be greater than zero.")

        return float(salary)

    def _validate_status(self, status: EmployeeStatus) -> EmployeeStatus:
        if not isinstance(status, EmployeeStatus):
            raise ValueError("Invalid employee status.")

        return status

    def deactivate(self) -> None:
        """
            Marks the employee as inactive.

            Employee records are never permanently deleted.
            This supports historical reporting and analytics.
        """
        self.status = EmployeeStatus.INACTIVE

    def to_dict(self) -> dict:
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department_id": self.department_id,
            "salary": self.salary,
            "manager_id": self.manager_id,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        employee = cls(
            name=data["name"],
            department_id=data["department_id"],
            salary=data["salary"],
            manager_id=data.get("manager_id"),
            status=EmployeeStatus(data["status"]),
        )

        employee._employee_id = data["employee_id"]

        numeric_id = int(employee.employee_id.replace("EMP", ""))
        if numeric_id >= cls.next_employee_id:
            cls.next_employee_id = numeric_id + 1

        return employee

    def __str__(self) -> str:
        return (
            f"{self.employee_id} | {self.name} | "
            f"{self.department_id} | {self.salary:.2f} | {self.status.value}"
        )