ADR-005: Entities Own Their State Changes

Status

Accepted

Date

2026-07-20

Context

Domain entities such as Employee and Department contain business state that changes over time.

Examples include:

an employee’s salary,
employment status,
department assignment,
and a department’s name.

If external classes modify entity attributes directly, they can bypass validation and other business behaviour associated with the change.

This would weaken encapsulation, spread business rules across the system, and increase the risk of invalid state.

Decision

Each domain entity shall own the operations that change its internal state.

External objects, including the Company aggregate, must request changes through the entity’s public domain methods rather than assigning private attributes directly.

For example:

employee.change_salary(new_salary)
employee.deactivate()
employee.transfer_to(department_id)

The aggregate remains responsible for coordinating operations involving multiple entities, while each entity remains responsible for validating and applying changes to its own state.

Consequences
Positive
Business rules remain close to the state they protect.
Direct mutation of private attributes is avoided.
Entity behaviour is easier to test independently.
Internal implementation details remain encapsulated.
Changes can later include events, auditing, or additional validation without affecting callers.
Company is less likely to become a God Object.
Trade-offs
More domain methods must be designed and maintained.
Some operations involve coordination between the aggregate and an entity.
Developers must understand which rules belong to the aggregate and which belong to the entity.
Review

This decision should be reconsidered if:

an operation does not naturally belong to one entity,
rules span several aggregates,
or a dedicated domain service becomes a clearer owner of the behaviour.

Until then, entities remain responsible for changing their own internal state.

Related Decisions
ADR-001: Company is the Aggregate Root
ADR-002: Encapsulate Aggregate State