Title

Employee Stores Department by Reference

Status: ✅ Accepted

Date: 2026-07-09 (or the actual implementation date in the project)

Context

The system requires every employee to belong to a department.

The architecture team considered two options:

Option A

The Employee object contains a complete Department object.

Option B

The Employee object stores only the department_id, with the Department object managed separately.

Decision

The Employee class shall store only the department_id.

The Company class will resolve the relationship between employees and departments when needed.

Rationale

This design:

avoids duplicated department information
follows database normalization principles
allows department details to change without modifying employee records
keeps the Employee class lightweight
aligns naturally with SQL foreign key relationships
simplifies future migration from JSON to SQL
Consequences
Advantages

✅ Single source of truth for department information

✅ Easier maintenance

✅ Better scalability

✅ Cleaner architecture