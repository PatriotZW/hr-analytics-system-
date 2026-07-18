"""
Company Repository Module

Purpose
-------
Provides a bridge between two representations
(domain and storage).

Responsibilities
----------------
- Accept a Company.
- Create a storage-friendly dictionary.
- Call the appropriate serialization method on each Department and Employee.
- Pass data to JsonStorage.save().
- Load raw dictionary data from storage.
- Reconstruct departments and employees.
- Register them with a new Company in the correct order.

Does Not
--------
- Open files directly.
- Validate employee or department attributes.
- Enforce new business rules.
- Choose its own storage path.
"""

# ============================================================
# Local Application Imports
# ============================================================

from models.company import Company
from models.department import Department
from models.employee import Employee
from storage.json_storage import JsonStorage


class CompanyRepository:
    """
    Coordinates persistence of the Company aggregate.

    The repository converts between domain objects and
    storage-friendly Python data structures.
    """

    def __init__(self, storage: JsonStorage):
        """
        Creates a CompanyRepository.

        Args:
            storage:
                JsonStorage dependency used for persistence.

        Raises:
            TypeError:
                If storage is not a JsonStorage object.
        """
        if not isinstance(storage, JsonStorage):
            raise TypeError("storage must be a JsonStorage object.")
        
        self._storage = storage

    @property
    def storage(self) -> JsonStorage:
        """
        Returns the repository's storage dependency.

        Returns:
            JsonStorage:
                The storage component used by the repository.
        """
        return self._storage

    
    def save(self, company: Company) -> None:
        """
        Saves a Company aggregate using the configured storage component.

        Args:
            company:
                Company aggregate to persist.

        Returns:
            None:
                This method does not return a value.

        Raises:
            TypeError:
                If company is not a Company object.
        """

        if not isinstance(company, Company):
            raise TypeError("company must be a Company object.")

        self.storage.save(company.to_dict())

        return None
    
    def load(self) -> Company:
        """
        Loads and reconstructs a Company aggregate.

        Returns:
            Company:
                The Company aggregate reconstructed from storage.

        Raises:
            FileNotFoundError:
                If the configured storage file does not exist.

            ValueError:
                If the stored Company relationships cannot be resolved.
        """

        data = self.storage.load()

        company = Company.from_dict(data)

        return company              # return Company.from_dict(self.storage.load())
    
"""
    It also makes debugging easier because you can inspect data separately from company.

We do not catch the exceptions here:

JsonStorage.load() reports missing or invalid storage.
Company.from_dict() reports invalid aggregate relationships.
CompanyRepository.load() coordinates and allows those errors to propagate honestly.

After adding the method, the next step is testing the repository itself: constructor validation, save(), load(), and the full save-load round trip.

"""
