ADR-009 — Single Company Scope

Context

The HR Analytics System requires a top-level object to coordinate employees and departments.

A decision is required on whether the system supports one or many companies.

Decision

Version 1.0 of the HR Analytics System supports exactly one Company.

The Company object is the root of the domain model.

Consequences

Advantages
Simpler architecture.
Simpler storage.
Simpler reporting.
Easier testing.
Clear ownership of employees and departments.
Trade-offs

The system cannot manage multiple organisations without future architectural changes.

Future

Support for multiple companies can be introduced by adding a higher-level object (or service) that coordinates multiple Company objects.


ADR-009 — Single Company Scope

Status: ✅ Accepted

Context

The HR Analytics System requires a top-level object to coordinate employees and departments.

A decision is required on whether Version 1.0 supports a single company or multiple companies.

Decision

The HR Analytics System Version 1.0 supports exactly one Company.

The Company class represents one organisation.

The application is responsible for ensuring that only one Company instance is registered.

Consequences
Advantages
Simpler architecture.
Simpler storage model.
Simpler reporting.
Clear ownership of all employees and departments.
Easier testing and maintenance.
Trade-offs

The system cannot manage multiple organisations in Version 1.0.

Supporting multiple companies would require introducing a higher-level coordinator (for example, an HRSystem class) in a future version.

Rationale

The Company class should not know whether another Company exists.

That is not its responsibility.

Instead, the application layer enforces the rule:

No Company Registered
        │
        ▼
Register Company
        │
        ▼
Company Exists
        │
        ▼
Second Registration Attempt
        │
        ▼
ValueError

This keeps the Company class cohesive while allowing future expansion to a multi-company architecture without modifying the Company model.
