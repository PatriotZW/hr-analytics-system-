ADR-010 — Separate Persistence Responsibility

Decision

Introduce a dedicated persistence component responsible for saving and loading system data.

Why

Employee should represent and protect employee data.
Department should represent and protect department data.
Company should coordinate organisational relationships.
None of them should know about JSON files, folders, or database connections.

This follows the Single Responsibility Principle and keeps the domain layer independent of the storage technology.