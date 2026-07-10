
"""
Department Module

Purpose
-------
Represents departments within the HR Analytics System.

Responsibilities
----------------
- Define the Department model.
- Validate department data.
- Manage department state.
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

# ============================================================
# Constants
# ============================================================

class DepartmentStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

MIN_DEPARTMENT_NAME_LENGTH = 2
MAX_DEPARTMENT_NAME_LENGTH = 100

STARTING_DEPARTMENT_ID = 1

DEPARTMENT_ID_PREFIX = "DEP"
DEPARTMENT_ID_NUMBER_LENGTH = 3

class Department:
    """
    Represents a single department within the organisation.

    Responsibilities
    ----------------
    - Maintain valid department information.
    - Protect object integrity.
    - Support serialization.

    A Department object should never exist in an invalid state.
    """

    next_department_id = STARTING_DEPARTMENT_ID

    def __init__(
        self,
        name: str,
        status: DepartmentStatus = DepartmentStatus.ACTIVE,
        ):
        """
        Creates a new Department object.

        Each Department is created in a valid state.
        Validation is performed before values are assigned.

        Args:
            name: Department's full name.
            status: Employment status.
        """
         
        # Validate and assign department attributes.
        self.name = self._validate_name(name)
        self.status = self._validate_status(status)  

        # Generate a unique department identifier.
        self._department_id = self._generate_department_id()

    @property
    def department_id(self) -> str:
        """
        Returns the department's unique identifier.

        The department ID is immutable and cannot be modified
        after the department has been created.
        """
        return self._department_id

    @classmethod
    def _generate_department_id(cls) -> str:
        """
        Generates the next available department identifier.

        Returns:
            str: The generated department ID.
        """

        department_id = (f"{DEPARTMENT_ID_PREFIX}" f"{cls.next_department_id:03d}")
        cls.next_department_id += 1
        return department_id
    
    @staticmethod
    def _validate_name(name: str) -> str:
        """
        Validates and cleans a department's name.

        Args:
            name: Department name entered by the user.

        Returns:
            str: The validated and formatted department name.

        Raises:
            ValueError: If the name is invalid.
        """
        
        stripped_name = name.strip().title()

        if not stripped_name:
            raise ValueError("Department name cannot be blank.")
         
        name_length = len(stripped_name)

        if not (MIN_DEPARTMENT_NAME_LENGTH <= name_length <= MAX_DEPARTMENT_NAME_LENGTH):
            raise ValueError(f"Department name must be between "
                             f"{MIN_DEPARTMENT_NAME_LENGTH} and {MAX_DEPARTMENT_NAME_LENGTH} characters.")
                
        return stripped_name
    
    @staticmethod
    def _validate_status(status: DepartmentStatus) -> DepartmentStatus:
        """
        Validates a department's status.

        Args:
            status: Department status assigned to the department.

        Returns:
            DepartmentStatus: The validated department status.

        Raises:
            ValueError: If the status is invalid.
        """

        if not isinstance(status, DepartmentStatus):
            raise ValueError("Invalid department status.")

        return status

    def deactivate(self) -> None:
        """
        Marks the department as inactive.

        This operation is idempotent. Calling it multiple
        times leaves the department in the same inactive state.
        """

        self.status = DepartmentStatus.INACTIVE

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        """
        Reconstructs a Department object from stored dictionary data.

        Args:
            data: Dictionary containing the stored department data.

        Returns:
            Department: Department data suitable for object creation.
        """

        department = cls(
            name=data["name"],
           status=DepartmentStatus(data["status"]),
            )

        department._department_id = data["department_id"]

        numeric_id = int(department.department_id.replace(DEPARTMENT_ID_PREFIX, ""))

        if numeric_id >= cls.next_department_id:
            cls.next_department_id = numeric_id + 1

        return department


    def to_dict(self) -> dict:
        """
        Converts the department object into a storage-friendly dictionary.

        Returns:
            dict: Department data suitable for JSON storage.
        """

        return {
            "department_id": self.department_id,
            "name": self.name,
            "status": self.status.value,
        }

    def __str__(self) -> str:
        """
        Returns a business-friendly string representation of the department.

        Returns:
            str: Formatted department details for display.
        """
        return(
            f"Department ID   : {self.department_id}\n"
            f"Name            : {self.name}\n"
            f"Status          : {self.status.value}"
        )