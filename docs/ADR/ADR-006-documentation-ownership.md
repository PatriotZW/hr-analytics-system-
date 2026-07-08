ADR-006 — Documentation Ownership

Decision:

Module docstrings describe the module's purpose, responsibilities, and boundaries.
Project metadata (version, author, history) is maintained by repository-level tooling and documentation (Git, README, releases), not duplicated in source files.

Reason:

Avoid duplication.
Keep documentation current.
Respect the single source of truth principle.