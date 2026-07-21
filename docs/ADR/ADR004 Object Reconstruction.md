ADR-004: Object Reconstruction

Status

Accepted

Date

2026-07-20

Context

The HR Analytics Platform persists domain objects outside the application. When data is loaded, the object graph must be reconstructed into valid Company, Department, and Employee instances.

Reconstruction is different from executing normal business operations. A persisted employee already exists; loading that employee is not equivalent to hiring a new employee.

Allowing repositories to modify object internals directly would bypass the domain model and tightly couple persistence code to the implementation of domain entities.

Likewise, reconstructing objects through ordinary business operations could trigger validations, events, timestamps, or workflows intended only for new business activities.

Decision

The domain model shall provide explicit reconstruction mechanisms for rebuilding valid objects from persisted data.

Repositories are responsible for:

reading persisted data,
translating storage formats,
invoking reconstruction methods.

The domain model is responsible for:

validating domain invariants,
restoring a valid object graph,
protecting encapsulated state.

Repositories must not directly manipulate private attributes.

Consequences
Positive
Business workflows remain separate from persistence workflows.
Domain invariants are preserved during reconstruction.
Repositories remain independent of object internals.
The domain retains ownership of object creation and validity.
Historical state can be restored without triggering unintended business behaviour.
Data integrity is maintained across persistence boundaries.
Trade-offs
Additional reconstruction methods must be implemented and maintained.
Repository implementations become slightly more complex.
Reconstructing large object graphs requires careful coordination.
Review

This decision should be revisited if:

a different persistence strategy requires alternative reconstruction techniques,
immutable domain objects become the preferred design,
or an ORM or event sourcing framework provides equivalent guarantees while preserving domain integrity.

Until then, reconstruction remains a responsibility of the domain model rather than the repository.

Related Decisions
ADR-001: Company is the Aggregate Root
ADR-002: Encapsulate Aggregate State
ADR-003: Separate Persistence from the Domain