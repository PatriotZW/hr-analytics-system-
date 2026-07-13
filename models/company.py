"""
Company Module

Purpose
-------
Represents the organisation within the HR Analytics System.

Responsibilities
----------------
- Coordinate employees and departments.
- Maintain organisational state.
- Enforce company-level business rules.

Does Not
--------
- Validate employee details.
- Validate department details.
- Persist data.
- Generate reports.
- Perform analytics.
"""
# ============================================================
# Local Application Imports
# ============================================================

#from models.employee import Employee
from models.department import Department, DepartmentStatus
from models.employee import Employee, EmployeeStatus

# ============================================================
# Constants
# ============================================================

MIN_COMPANY_NAME_LENGTH = 2
MAX_COMPANY_NAME_LENGTH = 100


class Company:
    """
    Represents the organisation.

    Responsibilities
    ----------------
    - Coordinate employees.
    - Coordinate departments.
    - Maintain organisational integrity.

    A Company object manages relationships between
    domain objects rather than replacing them.
    """
    def __init__(self, name: str):
        """
        Creates a new Company object.
        """
        self.name = self._validate_name(name)

        self._employees = []
        self._departments = []

    @property
    def departments(self) -> tuple[Department, ...]:
        """
        Returns the company's departments as a read-only collection.

        Returns:
            tuple[Department, ...]:
                Departments registered with the company.
        """

        return tuple(self._departments)


    @property
    def employees(self) -> tuple[Employee, ...]:
        """
        Returns the company's employees as a read-only collection.

        Returns:
            tuple[Employee, ...]:
                Employees registered with the company.
        """

        return tuple(self._employees)

    @staticmethod
    def _validate_name(name: str) -> str:
        """
        Validates and cleans the company's name.

        Args:
            name: Company name entered by the user.

        Returns:
            str: The validated and formatted company name.

        Raises:
            ValueError: If the name is invalid.
        """
        
        stripped_name = name.strip().title()

        if not stripped_name:
            raise ValueError("Company name cannot be blank.")
         
        name_length = len(stripped_name)

        if not (MIN_COMPANY_NAME_LENGTH <= name_length <= MAX_COMPANY_NAME_LENGTH):
            raise ValueError(f"Company name must be between "
                             f"{MIN_COMPANY_NAME_LENGTH} and {MAX_COMPANY_NAME_LENGTH} characters.")
                
        return stripped_name

    def add_department(self, department: Department) -> None:
        """
        Adds a department to the company.

        Args:
            department: Department object to add.

        Raises:
            TypeError: If the supplied value is not a Department object.
            ValueError: If the department ID or name already exists.
        """

        if not isinstance(department, Department):
            raise TypeError("department must be a Department object.")

        for existing_department in self._departments:
            if existing_department.department_id == department.department_id:
                raise ValueError(
                    f"Department ID {department.department_id} already exists."
                )

            if existing_department.name.casefold() == department.name.casefold():
                raise ValueError(
                    f"Department name '{department.name}' already exists."
                )

        self._departments.append(department)
                

    def add_employee(self, employee: Employee) -> None:
        """
        Adds an employee to the company.

        Args:
            employee: Employee object to add.

        Raises:
            TypeError: If the supplied value is not an Employee object.
            ValueError: If the employee ID already exists, the department
                does not exist, the manager does not exist, or the employee
                is assigned as their own manager.
        """

        if not isinstance(employee, Employee):
            raise TypeError("employee must be an Employee object.")

        for existing_employee in self._employees:
            if existing_employee.employee_id == employee.employee_id:
                raise ValueError(
                    f"Employee ID {employee.employee_id} already exists."
                )
        
        department = self.find_department_by_id(employee.department_id)

        if department is None:
            raise ValueError(
                f"Department ID {employee.department_id} does not exist."
            )

        if employee.manager_id is not None:
            if employee.manager_id == employee.employee_id:
                raise ValueError("An employee cannot manage themselves.")

            manager = self.find_employee_by_id(employee.manager_id)

            if manager is None:
                raise ValueError(
                    f"Manager ID {employee.manager_id} does not exist."
                )

        self._employees.append(employee)
        


    def find_department_by_id(self,department_id: str,) -> Department | None:
        """
        Finds a department by its unique identifier.

        Args:
            department_id: Department identifier to search for.

        Returns:
            Department | None:
                The matching Department if found,
                otherwise None.

        Raises:
            TypeError: If department_id is not a string.
        """
        if not isinstance(department_id, str):
            raise TypeError(
                "department_id must be a string."
            )

        cleaned_id = department_id.strip().upper()

        for department in self._departments:
            if department.department_id == cleaned_id:
                return department

        return None


    def find_employee_by_id(self,employee_id: str,) -> Employee | None:
        """
        Finds an employee by its unique identifier.

        Args:
            employee_id: Employee identifier to search for.

        Returns:
            Employee | None:
                The matching Employee if found,
                otherwise None.

        Raises:
            TypeError: If employee_id is not a string.
        """
        if not isinstance(employee_id, str):
            raise TypeError(
                "employee_id must be a string."
            )

        cleaned_id = employee_id.strip().upper()

        for employee in self._employees:
            if employee.employee_id == cleaned_id:
                return employee
        return None

    def deactivate_department(self, department_id: str) -> None:
        """
        Deactivates a department provided it has no active employees assigned to it.

        Args:
            department_id:
                Unique identifier of the department to deactivate.

        Returns:
            None:
                This method does not return a value.

        Raises:
            TypeError:
                If department_id is not a string.

            ValueError:
                If the department does not exist or has active employees
                assigned to it.
        """
        if not isinstance(department_id, str):
            raise TypeError(
                "department_id must be a string."
            )

        cleaned_id = department_id.strip().upper()

        department = self.find_department_by_id(cleaned_id)

        if department is None:
            raise ValueError(
                f"Department ID {cleaned_id} does not exist."
            )

        if department.status == DepartmentStatus.INACTIVE:
            return None

        for employee in self._employees:
            if (
                employee.department_id == cleaned_id
                and employee.status == EmployeeStatus.ACTIVE
            ):
                raise ValueError(
                    "Department has active employees and cannot be deactivated."
                )

        department.deactivate()

        return None
    
    def deactivate_employee(self, employee_id: str) -> None:
        """
        Deactivates an employee if they exist and are currently active.

        Args:
            employee_id:
                Unique identifier of the employee to deactivate.

        Returns:
            None:
                This method does not return a value.

        Raises:
            TypeError:
                If employee_id is not a string.

            ValueError:
                If the employee does not exist.
        """
        if not isinstance(employee_id, str):
            raise TypeError(
                "employee_id must be a string."
            )

        cleaned_id = employee_id.strip().upper()

        employee = self.find_employee_by_id(cleaned_id)

        if employee is None:
            raise ValueError(
                f"Employee ID {cleaned_id} does not exist."
            )

        if employee.status == EmployeeStatus.INACTIVE:
            return None

        employee.deactivate()

        return None
    

    def __str__(self) -> str:
        """
        Returns a business-friendly summary of the company.

        Returns:
            str: Formatted company details.
        """

        return (
            f"Company     : {self.name}\n"
            f"Departments : {len(self._departments)}\n"
            f"Employees   : {len(self._employees)}"
        )