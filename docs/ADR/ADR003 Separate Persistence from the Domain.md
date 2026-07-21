ADR-003: Separate Persistence from the Domain

Status

Accepted

Date

2026-07-20

Context

The Company aggregate represents the business domain of the HR Analytics Platform. Its responsibility is to model business rules and coordinate business operations.

Persisting data to JSON files, databases, or external services is an infrastructure concern rather than a business concern.

If persistence logic were implemented inside the domain model, every change in storage technology would require modifications to business classes.

For example, moving from JSON to SQLite, PostgreSQL, or a REST API would require changes to Company, even though the underlying business behaviour remains unchanged.

This would tightly couple the domain model to a specific storage mechanism and make testing more difficult.

Decision

Persistence responsibilities are delegated to Repository classes.

The domain model does not know:

where data is stored,
how it is stored,
or which storage technology is used.

Repositories translate between domain objects and the persistence layer.

Consequences
Positive
Business logic remains independent of storage technology.
Storage implementations can be replaced without modifying the domain model.
JSON, SQLite, PostgreSQL, cloud databases, or web services can be introduced with minimal impact on business code.
Unit tests for the domain model do not require file systems or databases.
Repository implementations can be tested independently from business rules.
Responsibilities remain clearly separated between the Domain and Infrastructure layers.
Trade-offs
Additional repository classes must be maintained.
Object reconstruction introduces additional complexity.
More abstractions are required than in a simple CRUD application.
Review

This decision should be revisited if:

persistence requirements become significantly more complex,
multiple data sources require different repository strategies,
or the architecture adopts an ORM or event-sourced persistence model.

Until then, repositories remain the only mechanism through which domain objects are persisted.

Related Decisions
ADR-001: Company is the Aggregate Root
ADR-002: Encapsulate Aggregate State
ADR-004: Object Reconstruction