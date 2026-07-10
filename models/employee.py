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

# ============================================================
# Standard Library Imports
# ============================================================

from enum import Enum
from typing import Optional


class EmployeeStatus(Enum):

    """
   Represents the employment status of 
   an employee.
    """

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

# ============================================================
# Constants
# ============================================================

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100

DEPARTMENT_ID_PREFIX = "DEP"
DEPARTMENT_ID_NUMBER_LENGTH = 3

STARTING_EMPLOYEE_ID = 1000

EMPLOYEE_ID_PREFIX = "EMP"
EMPLOYEE_ID_NUMBER_LENGTH = 4

class Employee:
    """
    Represents a single employee within the organisation.

    Responsibilities
    ----------------
    - Maintain valid employee information.
    - Protect object integrity.
    - Support serialization.

    An Employee object should never exist in an invalid state.
    """

    next_employee_id = STARTING_EMPLOYEE_ID

    def __init__(
        self,
        name: str,
        department_id: str,
        salary: float,
        manager_id: Optional[str] = None,
        status: EmployeeStatus = EmployeeStatus.ACTIVE,
    ):
        """
        Creates a new Employee object.

        Every Employee is created in a valid state.
        Validation is performed before values are assigned.

        Args:
            name: Employee's full name.
            department_id: Department reference.
            salary: Employee salary.
            manager_id: Manager reference.
            status: Employment status.
        """

        # Validate and assign employee attributes.
        self.name = self._validate_name(name)
        self.department_id = self._validate_department_id(department_id)
        self.salary = self._validate_salary(salary)
        self.manager_id = self._validate_manager_id(manager_id)
        self.status = self._validate_status(status)  

        # Generate a unique employee identifier.
        self._employee_id = self._generate_employee_id()
 
    @property
    def employee_id(self) -> str:
        """
        Returns the employee's unique identifier.

        The employee ID is immutable and cannot be modified
        after the employee has been created.
        """
        return self._employee_id

    @classmethod
    def _generate_employee_id(cls) -> str:
        """
        Generates the next available employee identifier.

        Returns:
            str: The generated employee ID.
        """

        employee_id = f"EMP{cls.next_employee_id}"
        cls.next_employee_id += 1
        return employee_id

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """
        Reconstructs an Employee object from stored dictionary data.

        Args:
            data: Dictionary containing the stored employee data.

        Returns:
            Employee: Employee data suitable for object creation.
        """

        employee = cls(
            name=data["name"],
            department_id=data["department_id"],
            salary=data["salary"],
            manager_id=data.get("manager_id"),
            status=EmployeeStatus(data["status"]),
                    )

        employee._employee_id = data["employee_id"]

        numeric_id = int(employee.employee_id.replace(EMPLOYEE_ID_PREFIX, ""))

        if numeric_id >= cls.next_employee_id:
            cls.next_employee_id = numeric_id + 1

        return employee

    @staticmethod
    def _validate_name(name: str) -> str:
        """
        Validates and cleans an employee's name.

        Args:
            name: Employee name entered by the user.

        Returns:
            str: The validated and formatted employee name.

        Raises:
            ValueError: If the name is invalid.
        """
        
        stripped_name = name.strip().title()

        if not stripped_name:
            raise ValueError("Employee name cannot be blank.")
         
        name_length = len(stripped_name)

        if not (MIN_NAME_LENGTH <= name_length <= MAX_NAME_LENGTH):
            raise ValueError(f"Employee name must be between "
                             f"{MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters.")
        
        
        return stripped_name

    @staticmethod
    def _validate_department_id(department_id: str) -> str:
        """
        Validates and cleans a department ID.

        Args:
            department_id: Department reference assigned to the employee.

        Returns:
            str: The validated and formatted department ID.

        Raises:
            ValueError: If the department ID is invalid.
        """
        DEPARTMENT_ID_PREFIX = "DEP"
        DEPARTMENT_ID_NUMBER_LENGTH = 3


        department_id = department_id.strip().upper()

        if not department_id:
            raise ValueError("Department can not be blank.")
                    
        if not department_id.startswith(DEPARTMENT_ID_PREFIX):
            raise ValueError(f"Department should start with {DEPARTMENT_ID_PREFIX}.")
    
        department_length = len(department_id)

        accepted_department_length = (len(DEPARTMENT_ID_PREFIX)  + DEPARTMENT_ID_NUMBER_LENGTH)

        if department_length != accepted_department_length:
            raise ValueError(f"Department must be {accepted_department_length} characters.")
        
        if not department_id[len(DEPARTMENT_ID_PREFIX):].isdigit(): 
            raise ValueError(f"Department must be {DEPARTMENT_ID_NUMBER_LENGTH} numbers")   
            
        return department_id


    @staticmethod
    def _validate_salary(salary: float) -> float:
            """
            Validates salary.

            Args:
                salary: salary for the employee.

            Returns:
                float: The validated salary.

            Raises:
                ValueError: If the salary is invalid.
            """
            
            if not isinstance(salary, (int, float)):
                raise ValueError("Salary must be an int or float.")
        
            if salary <= 0:
                raise ValueError(f"Salary {salary} is zero or less")
            
            return salary




    @staticmethod
    def _validate_manager_id(manager_id: Optional[str]) -> Optional[str]:
        """
        Validates and cleans a manager ID.

        Args:
            manager_id: Employee ID of the employee's manager.

        Returns:
            Optional[str]: The validated manager ID, or None if no manager is assigned.

        Raises:
            ValueError: If the manager ID is invalid.

        manager_id is optional
        """

        if manager_id is None:
            return None
        
        manager_id = manager_id.strip().upper()
        
        if not manager_id:
            raise ValueError("Manager can not be blank.")
            
        if not manager_id.startswith(EMPLOYEE_ID_PREFIX):
            raise ValueError(f"Manager should start with {EMPLOYEE_ID_PREFIX}.")
        
        manager_length = len(manager_id)
        expected_employee_id_length = (len(EMPLOYEE_ID_PREFIX) + EMPLOYEE_ID_NUMBER_LENGTH)
        
        if manager_length != expected_employee_id_length:
            raise ValueError(f"Manager must be {expected_employee_id_length} characters.")
            
        if not manager_id[len(EMPLOYEE_ID_PREFIX):].isdigit(): 
            raise ValueError(f"Manager must be {EMPLOYEE_ID_NUMBER_LENGTH} numbers")   
                
        return manager_id


    @staticmethod
    def _validate_status(status: EmployeeStatus) -> EmployeeStatus:
        """
        Validates an employee status.

        Args:
            status: Employment status assigned to the employee.

        Returns:
            EmployeeStatus: The validated employee status.

        Raises:
            ValueError: If the status is invalid.
        """

        if not isinstance(status, EmployeeStatus):
            raise ValueError("Invalid employee status.")

        return status

    def deactivate(self) -> None:
        """
        Marks the employee as inactive.

        This operation is idempotent. Calling it multiple
        times leaves the employee in the same inactive state.
        """
            
        self.status = EmployeeStatus.INACTIVE

    def to_dict(self) -> dict:
        """
        Converts the employee object into a storage-friendly dictionary.

        Returns:
            dict: Employee data suitable for JSON storage.
        """

        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department_id": self.department_id,
            "salary": self.salary,
            "manager_id": self.manager_id,
            "status": self.status.value,
            }
    
    
    def __str__(self) -> str:
        """
        Returns a business-friendly string representation of the employee.

        Returns:
            str: Formatted employee details for display.
        """

        manager = self.manager_id if self.manager_id else "Not Assigned"

        return (
            f"Employee ID : {self.employee_id}\n"
            f"Name        : {self.name}\n"
            f"Department  : {self.department_id}\n"
            f"Salary      : {self.salary:.2f}\n"
            f"Manager     : {manager}\n"
            f"Status      : {self.status.value}"
        )