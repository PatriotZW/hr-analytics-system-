ADR-007 — Generate Employee ID After Validation

Decision:
Employee IDs are assigned only after all constructor validation succeeds.

Reason:
- prevents ID gaps from failed employee creation
- aligns with business onboarding logic
- ensures only accepted employee records receive IDs



ADR-007 – Generate Employee ID After Validation

Status: ✅ Accepted

Context

Initially, the Employee constructor generated an employee_id before validating the employee's data.

This created a problem:

Generate EMP1006
        ↓
Validate salary
        ↓
Validation fails
        ↓
Employee not created

The next employee would receive:

EMP1007

leaving an unnecessary gap.

Decision

The Employee class shall:

Validate all constructor arguments.
Assign validated values to the object.
Generate the employee_id only after all validation succeeds.

The constructor now follows this sequence:

Validate Name
        ↓
Validate Department
        ↓
Validate Salary
        ↓
Validate Manager
        ↓
Validate Status
        ↓
Generate Employee ID
Consequences
Advantages
Only successfully created employees receive an ID.
No gaps caused by failed validation.
Reflects the real HR onboarding process.
Easier to reason about during testing.
Keeps employee identity tied to successful creation.
Trade-offs

Future database-backed systems may use database-generated identities that can legitimately contain gaps. When that architecture is introduced, this ADR may be revisited.

Rationale

The decision models real-world business processes:

A passport number is assigned after an application is approved.
A bank account number is assigned after all checks are complete.
Likewise, an employee ID should be assigned only after the employee has successfully passed all business validation.