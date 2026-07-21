ADR-002: Encapsulate Aggregate State

Status

Accepted

Date

2026-07-20

Context

The Company aggregate maintains internal collections of employees and departments.

When these collections were exposed as public mutable lists, external code could modify them directly using operations such as append(), remove(), or item assignment.

Direct mutation would bypass the business rules and validation implemented by the aggregate. For example, a developer could add an employee without checking for duplicate identifiers, validating the department, or updating all related state consistently.

This created a risk that the aggregate could enter an invalid or inconsistent state.

Decision

The internal collections of the Company aggregate will remain private and mutable within the class:

self._employees
self._departments

External consumers will receive read-only views through properties:

@property
def employees(self) -> tuple[Employee, ...]:
    return tuple(self._employees)

@property
def departments(self) -> tuple[Department, ...]:
    return tuple(self._departments)

All changes to these collections must be performed through controlled domain operations provided by the aggregate.

Consequences
Positive
External code cannot directly mutate aggregate collections.
Business validation cannot be bypassed through normal use of the public API.
Aggregate invariants are protected.
State changes occur through clearly defined operations.
The source of mutations is easier to trace and test.
Future changes to the internal collection implementation will have less impact on consumers.
Trade-offs
A new tuple is created whenever a property is accessed.
Developers must use domain methods rather than convenient list operations.
The class must provide appropriate methods for every legitimate mutation.
Python does not provide absolute privacy, so disciplined use of the public API is still required.
Review

This decision should be revisited if:

collection size makes repeated tuple creation a measurable performance issue,
consumers require a different read-only collection abstraction,
or the aggregate boundary changes.

Until then, aggregate collections remain private and are exposed only through read-only views.

Related Decisions
ADR-001: Company is the Aggregate Root
ADR-005: Entity-Owned State Changes