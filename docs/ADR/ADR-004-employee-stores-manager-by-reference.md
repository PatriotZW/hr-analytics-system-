ADR-004
Employee Stores Manager by Reference

Title

Employee Stores Manager by Reference

Status: ✅ Accepted

Version: 1.0

Context

Every employee reports to a manager.

A manager is also an employee.

The architecture team considered two options:

Option A

Store a complete Manager object inside every Employee.

Option B

Store only the manager_id, referencing another employee.

Decision

The Employee class shall store only the manager_id.

The relationship between employees and managers shall be resolved by the Company class.

Rationale
Maintains a single source of truth for manager information.
Prevents duplicated manager data.
Supports SQL self-referencing relationships.
Simplifies updates to manager information.
Reduces memory usage and object duplication.
Keeps the object model consistent with future database design.
Consequences
Advantages
One manager record.
Unlimited reporting hierarchy.
Easy SQL migration.
Easier analytics.
Cleaner architecture.
Trade-offs

Resolving a manager requires a lookup through the Company class.

This is acceptable because the benefits of data integrity outweigh the additional lookup.