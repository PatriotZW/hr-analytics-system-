ADR-001: Company is the Aggregate Root

Status

Accepted

Date

2026-07-20

Context

The HR Analytics Platform contains several related domain entities, including Company, Department, and Employee.

Many business operations affect more than one entity at the same time. Examples include:

Hiring an employee
Transferring an employee between departments
Assigning a manager
Deactivating an employee

If these operations were performed directly by Employee or Department, responsibilities would become blurred. Individual entities would need knowledge of other entities, increasing coupling and making it easier for the system to enter an inconsistent state.

Decision

Company shall act as the Aggregate Root of the HR domain.

All business operations involving multiple entities will be initiated through Company.

Employee and Department will remain responsible only for maintaining and validating their own state and behaviour.

Consequences
Positive
Clear separation of responsibilities.
Cross-entity business rules are enforced consistently.
Individual entities remain focused and easier to maintain.
Reduced coupling between domain entities.
Lower risk of inconsistent business state.
Simpler testing of business workflows.
Trade-offs
Company becomes responsible for coordinating business operations.
Care must be taken to ensure Company does not evolve into a "God Object". As the platform grows, coordination logic may be delegated to domain services where appropriate while Company remains the Aggregate Root.
Related Decisions
ADR-002: Entity Encapsulation
ADR-005: Entity-Owned State Changes