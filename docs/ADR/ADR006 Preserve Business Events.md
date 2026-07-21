ADR-006: Preserve Business Events

Status

Accepted

Date

2026-07-20

Context

Domain operations represent meaningful business occurrences as well as state changes.

Examples include:

EmployeeHired
EmployeeTransferred
SalaryChanged
EmployeeDeactivated

Other parts of the platform may need to react to these occurrences without being directly coupled to the domain operation that produced them.

If events are discarded too early, downstream actions such as analytics updates, payroll processing, auditing, onboarding, or notifications may not occur even though the domain state was successfully changed.

Decision

Domain entities and aggregates shall record business events produced by domain operations.

Events must remain available until the application layer explicitly retrieves and processes them.

Persistence and reconstruction must not create duplicate historical events.

Loading an existing employee is not a new EmployeeHired event.

After successful processing, handled events may be cleared from the aggregate.

A possible interface is:

@property
def domain_events(self) -> tuple[DomainEvent, ...]:
    return tuple(self._domain_events)

def clear_domain_events(self) -> None:
    self._domain_events.clear()
Consequences
Positive
Business side effects remain decoupled from domain logic.
New event handlers can be introduced without modifying core operations.
Important business occurrences remain observable.
Auditing and analytics become easier to support.
Domain behaviour can be tested independently from external integrations.
The architecture can later support messaging or event-driven workflows.
Trade-offs
Event processing introduces additional application-layer complexity.
Failed handlers require a retry or recovery strategy.
Care is needed to prevent duplicate event processing.
Saving state and publishing events may require transactional coordination.
Events must be versioned carefully as the platform evolves.
Review

This decision should be revisited when:

events are published through an external message broker,
reliable delivery becomes mandatory,
transactional outbox support is introduced,
or the system adopts event sourcing.

Until then, domain events remain in memory until explicitly processed and cleared by the application layer.

Related Decisions
ADR-003: Separate Persistence from the Domain
ADR-004: Object Reconstruction
ADR-005: Entities Own Their State Changes