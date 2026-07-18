ADR-011

Title

Separate Storage Mechanism from Repository

Status

Accepted

Context

The application requires persistent storage for domain
objects.

Storing JSON directly inside Company or future repository
classes would mix persistence mechanics with domain
coordination.

Decision

Introduce JsonStorage as a dedicated low-level component.

JsonStorage is responsible only for:

- Managing file paths
- Saving JSON-compatible data
- Loading JSON-compatible data

JsonStorage does not:

- Know about Employee
- Know about Department
- Know about Company
- Perform object serialization
- Apply business rules

Repositories will later coordinate between the
domain model and JsonStorage.

Consequences

Benefits

- Clear separation of responsibilities
- Reusable persistence component
- Easier testing
- Storage implementation can change independently