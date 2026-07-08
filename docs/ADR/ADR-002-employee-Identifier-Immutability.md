Title

Employee Identifier Immutability

Status

Accepted

Context

Every employee requires a unique identifier.

The identifier is referenced throughout the system and future integrations.

Decision

Employee IDs are:

automatically generated
unique
immutable

Once assigned, an employee ID cannot be changed.

Consequences

Advantages:

stable identity
reliable database relationships
simpler analytics
easier system integration

Trade-off:

If an employee ID is generated incorrectly (unlikely), the record must be recreated rather than edited.